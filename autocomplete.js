/* Autocomplete offline: 3.000 tarefas, nenhuma API, nenhuma transmissão de texto. */
(() => {
  'use strict';
  const input = document.getElementById('task');
  const tray = document.getElementById('task-suggestions');
  const list = document.getElementById('suggestions-list');
  const label = document.getElementById('suggestions-label');
  const status = document.getElementById('suggestions-status');
  if (!input || !tray || !list || !label || !status) return;

  const CATEGORY_LABELS = {
    learn: 'Aprender', creative: 'Criatividade', routine: 'Produtividade',
    highrisk: 'Decisão importante', personal: 'Expressão pessoal',
    sensitive: 'Privacidade', noai: 'Sem IA'
  };
  const catalog = Array.isArray(window.ANTES_TASKS) ? window.ANTES_TASKS : [];
  const indexed = catalog.map(item => ({
    ...item,
    normalized: normalize(item.task),
    words: normalize(item.task).split(' '),
    terms: tokens(item.task)
  }));
  const frequency = Object.create(null);
  for (const item of indexed) for (const term of item.terms) frequency[term] = (frequency[term] || 0) + 1;

  let items = [];
  let activeIndex = -1;
  let frame = 0;

  // Similaridade textual com variantes comuns e prefixos, inclusive palavras incompletas.
  // Não há embedding, modelo de linguagem nem envio da consulta a terceiros.
  function similarTasks(query, limit = 6) {
    const normalizedQuery = normalize(query);
    if (normalizedQuery.length < 3 || !indexed.length) return [];
    const terms = tokens(query);
    if (!terms.length) return [];
    const size = indexed.length;
    const weights = terms.map(term => Math.log(1 + size / (1 + (frequency[term] || 0))));
    const totalWeight = weights.reduce((sum, weight) => sum + weight, 0) || 1;
    const ranked = [];

    for (const row of indexed) {
      let matchingWeight = 0;
      let matchedTerms = 0;
      for (let i = 0; i < terms.length; i++) {
        const term = terms[i];
        let strength = 0;
        if (row.terms.includes(term)) strength = 1;
        else if (term.length >= 3 && row.terms.some(word => word.startsWith(term))) strength = .82;
        else if (term.length >= 3 && row.words.some(word => word.startsWith(term))) strength = .73;
        if (strength) { matchingWeight += weights[i] * strength; matchedTerms++; }
      }
      if (!matchedTerms) continue;

      const coverage = matchingWeight / totalWeight;
      const compactness = matchedTerms / Math.max(row.terms.length, 1);
      let score = coverage * .86 + Math.min(compactness, 1) * .06;
      if (row.normalized.includes(normalizedQuery)) score += .065;
      if (row.normalized.startsWith(normalizedQuery)) score += .055;
      if (row.normalized === normalizedQuery) score = 1.5;
      if (score < .24) continue;
      ranked.push({ id: row.id, task: row.task, category: row.category, score });
    }
    ranked.sort((a, b) => b.score - a.score || a.task.length - b.task.length || a.id.localeCompare(b.id));
    return ranked.slice(0, Math.max(1, Math.min(limit, 10)));
  }

  function hideSuggestions() {
    if (frame) { cancelAnimationFrame(frame); frame = 0; }
    tray.hidden = true;
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    list.replaceChildren();
    items = [];
    activeIndex = -1;
  }

  function setActive(index) {
    if (!items.length) return;
    activeIndex = (index + items.length) % items.length;
    for (const [i, button] of Array.from(list.children).entries()) {
      button.classList.toggle('is-active', i === activeIndex);
      button.setAttribute('aria-selected', String(i === activeIndex));
    }
    const selected = list.children[activeIndex];
    input.setAttribute('aria-activedescendant', selected.id);
    selected.scrollIntoView({ block: 'nearest' });
  }

  function selectTask(item) {
    // A recomendação usa exatamente a tarefa escolhida, mais o contexto opcional preenchido.
    input.value = item.task;
    document.getElementById('charcount').textContent = `${input.value.length} / 700`;
    document.getElementById('error').textContent = '';
    hideSuggestions();
    document.getElementById('task-form').requestSubmit();
  }

  function updateSuggestions() {
    frame = 0;
    const query = input.value.trim();
    if (query.length < 3) { hideSuggestions(); return; }
    items = similarTasks(query, 6);
    activeIndex = -1;
    list.replaceChildren();
    tray.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    input.removeAttribute('aria-activedescendant');

    if (!indexed.length) {
      label.textContent = 'Catálogo temporariamente indisponível';
      const msg = document.createElement('p');
      msg.className = 'suggestions-empty';
      msg.textContent = 'Ainda é possível analisar sua descrição usando as regras locais.';
      list.append(msg);
      status.textContent = 'Catálogo indisponível';
      return;
    }
    if (!items.length) {
      label.textContent = 'Nenhuma correspondência próxima';
      const msg = document.createElement('p');
      msg.className = 'suggestions-empty';
      msg.textContent = 'Continue descrevendo ou clique em “Analisar tarefa” para uma recomendação geral.';
      list.append(msg);
      status.textContent = 'Nenhuma tarefa semelhante encontrada';
      return;
    }

    label.textContent = `${items.length} tarefa${items.length === 1 ? '' : 's'} semelhante${items.length === 1 ? '' : 's'}`;
    status.textContent = `${items.length} sugestões disponíveis. Use as setas para navegar e Enter para selecionar.`;
    items.forEach((item, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.id = `suggestion-${index}`;
      button.className = 'suggestion';
      button.setAttribute('role', 'option');
      button.setAttribute('aria-selected', 'false');
      button.setAttribute('tabindex', '-1');
      const main = document.createElement('span');
      main.className = 'suggestion-text';
      main.textContent = item.task;
      const category = document.createElement('span');
      category.className = 'suggestion-category';
      category.textContent = CATEGORY_LABELS[item.category] || 'Tarefa';
      const arrow = document.createElement('span');
      arrow.className = 'suggestion-arrow';
      arrow.setAttribute('aria-hidden', 'true');
      arrow.textContent = '↗';
      button.append(main, category, arrow);
      button.addEventListener('mouseenter', () => setActive(index));
      button.addEventListener('click', () => selectTask(item));
      list.append(button);
    });
  }

  input.setAttribute('role', 'combobox');
  input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-controls', 'suggestions-list');
  input.setAttribute('aria-expanded', 'false');

  input.addEventListener('input', () => {
    if (frame) cancelAnimationFrame(frame);
    frame = requestAnimationFrame(updateSuggestions);
  });
  input.addEventListener('focus', () => {
    if (input.value.trim().length >= 3 && tray.hidden) {
      if (frame) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(updateSuggestions);
    }
  });
  input.addEventListener('keydown', event => {
    if (event.isComposing || event.keyCode === 229) return;
    if (event.key === 'Escape') { hideSuggestions(); return; }
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      if (!tray.hidden && items.length) {
        event.preventDefault();
        setActive(event.key === 'ArrowDown' ? activeIndex + 1 : activeIndex - 1);
      }
      return;
    }
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (!tray.hidden && items.length) selectTask(items[activeIndex < 0 ? 0 : activeIndex]);
      else document.getElementById('task-form').requestSubmit();
    }
  });
  document.getElementById('task-form').addEventListener('submit', hideSuggestions);
  document.addEventListener('pointerdown', event => {
    if (!document.getElementById('task-form').contains(event.target)) hideSuggestions();
  });
  window.__suggestTasks = similarTasks;
})();