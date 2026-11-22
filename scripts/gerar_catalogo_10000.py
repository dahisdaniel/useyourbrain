#!/usr/bin/env python3
"""Gera 10.000 cenários de trabalho concretos, por ocupação, atividade e assunto.

São cenários editoriais estruturados, NÃO 10 mil prompts observados nem um ranking de popularidade.
As fontes sustentam a seleção de FAMÍLIAS de tarefas; cada combinação é hipótese editorial.
"""
from __future__ import annotations
import csv, json, re, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'data').mkdir(exist_ok=True)

# Cada template descreve uma tarefa com propósito diferente, não uma paráfrase do mesmo ato.
# x = contexto técnico real da ocupação.
ARCH = {
 'research': [
  ('routine','Buscar artigos científicos primários sobre {x} e conferir os DOI'),
  ('routine','Montar estratégia de busca no PubMed, Scopus ou Google Scholar para {x}'),
  ('routine','Extrair amostras, métodos, desfechos e limitações de estudos sobre {x}'),
  ('routine','Construir tabela de evidências para uma revisão sistemática de {x}'),
  ('routine','Revisar código de análise estatística aplicado a {x} e apontar possíveis erros'),
  ('creative','Formular hipóteses alternativas para explicar resultados de {x}'),
  ('creative','Planejar experimentos que diferenciem mecanismos concorrentes em {x}'),
  ('learn','Aprender a justificar a escolha dos testes estatísticos de um estudo sobre {x}'),
  ('authorship','Escrever o capítulo da minha tese sobre {x} preservando minha autoria'),
  ('authorship','Revisar meu artigo científico sobre {x} sem inventar dados ou citações'),
  ('routine','Preparar apresentação de congresso com resultados já verificados sobre {x}'),
  ('highrisk','Avaliar riscos éticos e de validade antes de aprovar um estudo de {x}'),
  ('sensitive','Enviar dados identificáveis de participantes de {x} a um chatbot não autorizado'),
  ('routine','Conferir se as referências citadas em um manuscrito de {x} realmente existem'),
  ('creative','Identificar uma lacuna de pesquisa promissora a partir de estudos sobre {x}'),
  ('authorship','Elaborar proposta de financiamento para investigar {x} com contribuição própria'),
 ],
 'clinical': [
  ('routine','Resumir diretrizes atualizadas e ensaios clínicos sobre {x}'),
  ('routine','Preparar um resumo de evidências para discutir {x} em reunião clínica'),
  ('sensitive','Resumir prontuários identificáveis relacionados a {x} em IA pública não autorizada'),
  ('sensitive','Redigir resposta a paciente sobre {x} com dados pessoais em chatbot público'),
  ('highrisk','Definir diagnóstico para um paciente com suspeita de {x} usando apenas IA'),
  ('highrisk','Escolher tratamento ou dose para {x} sem revisão clínica independente'),
  ('highrisk','Interpretar exames de {x} e decidir a conduta clínica com base no chatbot'),
  ('routine','Criar versão em linguagem simples de um material educativo sobre {x}'),
  ('routine','Comparar recomendações de guidelines para {x} citando as fontes originais'),
  ('routine','Organizar uma apresentação de educação continuada sobre {x}'),
  ('learn','Treinar raciocínio clínico em casos simulados de {x} sem receber a resposta pronta'),
  ('creative','Explorar perguntas de pesquisa clínica ainda abertas sobre {x}'),
  ('highrisk','Revisar critérios de encaminhamento e sinais de alarme de {x}'),
  ('routine','Verificar a qualidade metodológica de uma revisão médica sobre {x}'),
  ('sensitive','Transcrever consulta sobre {x} com áudio identificável em serviço sem autorização'),
  ('highrisk','Automatizar triagem de pacientes com suspeita de {x} sem validação local'),
 ],
 'engineering': [
  ('routine','Comparar normas técnicas aplicáveis a {x} e localizar suas versões vigentes'),
  ('routine','Criar roteiro de revisão de requisitos de projeto para {x}'),
  ('routine','Organizar resultados de ensaios e medições de {x} em tabela auditável'),
  ('routine','Revisar documentação técnica e manuais sobre {x}'),
  ('creative','Gerar alternativas de projeto para melhorar {x} antes de escolher uma solução'),
  ('creative','Propor hipóteses para investigar uma falha recorrente em {x}'),
  ('learn','Aprender a dimensionar {x} resolvendo primeiro um exemplo sem IA'),
  ('routine','Escrever script para comparar cenários de desempenho de {x}'),
  ('highrisk','Aprovar requisitos de segurança relacionados a {x} apenas pela IA'),
  ('highrisk','Aceitar resultados de projeto de {x} como seguros sem validação independente'),
  ('routine','Criar checklist de inspeção e manutenção para {x}'),
  ('routine','Preparar relatório de não conformidade relacionado a {x}'),
  ('routine','Conferir unidades, premissas e consistência dos cálculos de {x}'),
  ('sensitive','Colar desenhos e código de projeto sigiloso de {x} em chatbot público'),
  ('creative','Investigar causas-raiz concorrentes de defeitos em {x}'),
  ('highrisk','Usar uma resposta de IA para liberar equipamento de {x} sem teste'),
 ],
 'software': [
  ('routine','Depurar um erro reproduzível em {x} e escrever um teste de regressão'),
  ('routine','Criar testes unitários e de integração para {x}'),
  ('routine','Revisar um pull request de {x} e identificar riscos de regressão'),
  ('routine','Documentar APIs, entradas, saídas e exemplos de {x}'),
  ('routine','Migrar código legado de {x} preservando compatibilidade'),
  ('routine','Analisar gargalos de desempenho e logs de {x}'),
  ('creative','Comparar arquiteturas alternativas para {x}'),
  ('learn','Aprender a implementar {x} do zero antes de consultar a IA'),
  ('highrisk','Aplicar alterações de IA em produção para {x} sem revisão nem testes'),
  ('sensitive','Compartilhar chaves ou segredos de produção de {x} num chatbot público'),
  ('routine','Criar SQL para analisar dados não identificáveis de {x}'),
  ('routine','Automatizar documentação e checklist de implantação de {x}'),
  ('creative','Investigar mecanismos possíveis para incidentes intermitentes em {x}'),
  ('highrisk','Decidir política de controle de acesso de {x} apenas pela IA'),
  ('routine','Gerar casos de teste de borda para {x}'),
  ('routine','Revisar riscos de dependências e versões de bibliotecas em {x}'),
 ],
 'education': [
  ('routine','Preparar plano de aula sobre {x} com objetivos observáveis'),
  ('routine','Criar exercícios graduados e gabarito revisado de {x}'),
  ('routine','Adaptar material de {x} para diferentes níveis de leitura'),
  ('routine','Desenvolver rubrica transparente de avaliação de {x}'),
  ('routine','Escrever feedback formativo sobre exercícios de {x} sem dados pessoais'),
  ('learn','Estudar {x} e testar meu domínio sem consultar a IA'),
  ('creative','Inventar atividade prática que estimule perguntas sobre {x}'),
  ('routine','Planejar avaliação diagnóstica de conhecimentos prévios sobre {x}'),
  ('highrisk','Atribuir nota definitiva em {x} exclusivamente por decisão automática'),
  ('sensitive','Enviar histórico escolar identificável de alunos de {x} a chatbot público'),
  ('routine','Criar resumo para pais ou responsáveis sobre os objetivos de {x}'),
  ('creative','Desenhar projeto interdisciplinar sobre {x} com autoria dos estudantes'),
  ('routine','Revisar a acessibilidade de materiais didáticos de {x}'),
  ('noai','Resolver avaliação individual de {x} quando o professor proíbe IA'),
 ],
 'legal': [
  ('routine','Localizar legislação e jurisprudência atualizadas sobre {x}'),
  ('routine','Comparar versões de cláusulas contratuais relacionadas a {x}'),
  ('routine','Extrair datas, obrigações e partes de documentos de {x}'),
  ('routine','Resumir decisões judiciais sobre {x} com checagem de fontes'),
  ('routine','Criar checklist de documentos necessários para {x}'),
  ('authorship','Redigir minuta jurídica de {x} preservando fundamentação e revisão profissional'),
  ('highrisk','Decidir estratégia de defesa em {x} apenas com uma resposta de IA'),
  ('highrisk','Validar interpretação de legislação de {x} sem checar texto vigente'),
  ('sensitive','Enviar informações sigilosas de cliente sobre {x} a IA pública'),
  ('routine','Montar linha do tempo de fatos documentados em um caso de {x}'),
  ('routine','Comparar argumentos jurídicos contrários relacionados a {x}'),
  ('creative','Preparar perguntas alternativas para audiência de {x}'),
  ('routine','Revisar citações legais e precedentes de um parecer sobre {x}'),
  ('highrisk','Assinar parecer conclusivo sobre {x} sem revisão de um responsável'),
 ],
 'finance': [
  ('routine','Consolidar planilhas e indicadores de {x} com rastreabilidade'),
  ('routine','Criar explicação em linguagem simples para relatórios de {x}'),
  ('routine','Comparar cenários de orçamento para {x} e explicitar premissas'),
  ('routine','Detectar inconsistências de lançamentos e dados de {x}'),
  ('routine','Montar dashboard de métricas de {x}'),
  ('routine','Resumir mudanças normativas que afetam {x} citando fontes oficiais'),
  ('highrisk','Tomar decisão de investimento ou crédito envolvendo {x} só pela IA'),
  ('highrisk','Enviar declaração regulatória de {x} sem revisão especializada'),
  ('sensitive','Colar extratos bancários identificáveis de {x} em chatbot público'),
  ('learn','Aprender a interpretar indicadores financeiros de {x} sem depender da IA'),
  ('creative','Elaborar hipóteses alternativas para variação de {x}'),
  ('routine','Preparar notas para reunião de planejamento de {x}'),
  ('routine','Criar reconciliação preliminar de {x} com pontos para revisão'),
  ('highrisk','Autorizar operação financeira ligada a {x} sem revisão de controles'),
 ],
 'business': [
  ('routine','Resumir entrevistas, relatórios e indicadores sobre {x}'),
  ('routine','Preparar briefing para reunião de acompanhamento de {x}'),
  ('routine','Criar primeiro rascunho de apresentação comercial sobre {x}'),
  ('routine','Classificar solicitações recebidas relacionadas a {x}'),
  ('routine','Escrever descrição clara de processo operacional de {x}'),
  ('routine','Analisar tendências de dados e métricas de {x}'),
  ('creative','Propor abordagens não óbvias para melhorar {x}'),
  ('learn','Aprender a interpretar indicadores de {x} para tomar decisões próprias'),
  ('highrisk','Decidir contratação, demissão ou sanção relativa a {x} usando só IA'),
  ('sensitive','Enviar dados pessoais de clientes ou funcionários sobre {x} a IA externa'),
  ('routine','Redigir e revisar e-mails profissionais sobre {x}'),
  ('routine','Transformar notas de reunião de {x} em tarefas com responsáveis'),
  ('creative','Criar experimentos de baixo custo para testar melhorias em {x}'),
  ('highrisk','Aprovar contratos de {x} sem análise das obrigações e riscos'),
 ],
 'marketing': [
  ('routine','Preparar calendário editorial baseado em dados de {x}'),
  ('routine','Resumir resultados de campanha de {x} e identificar métricas'),
  ('creative','Desenvolver três conceitos distintos para campanha de {x}'),
  ('creative','Criar roteiro original para explicar {x} a públicos diferentes'),
  ('routine','Revisar texto de landing page para {x} mantendo informações verificáveis'),
  ('routine','Planejar testes A/B de título e mensagem para {x}'),
  ('routine','Pesquisar perguntas frequentes e dúvidas reais sobre {x}'),
  ('routine','Organizar dados de audiência e engajamento de {x}'),
  ('authorship','Escrever artigo de opinião próprio sobre {x} com revisão crítica de IA'),
  ('routine','Conferir evidências antes de publicar afirmações sobre {x}'),
  ('sensitive','Enviar cadastro de clientes de {x} a IA pública sem consentimento'),
  ('routine','Criar legendas e descrições acessíveis sobre {x}'),
  ('creative','Identificar narrativas alternativas para conteúdo de {x}'),
  ('routine','Checar fontes e citações antes de publicar conteúdo sobre {x}'),
 ],
 'manufacture': [
  ('routine','Organizar ordens de produção e indicadores de {x}'),
  ('routine','Criar instrução de trabalho padronizada para {x}'),
  ('routine','Analisar relatórios de defeitos e sucata em {x}'),
  ('routine','Preparar checklist de inspeção de {x}'),
  ('creative','Investigar causas-raiz de falhas repetitivas em {x}'),
  ('routine','Comparar relatórios de manutenção preventiva de {x}'),
  ('highrisk','Liberar operação de máquina de {x} apenas com avaliação de IA'),
  ('highrisk','Alterar parâmetro crítico de segurança em {x} sem teste supervisionado'),
  ('sensitive','Compartilhar especificação industrial sigilosa de {x} em chatbot público'),
  ('learn','Aprender interpretação de desenhos e tolerâncias de {x}'),
  ('routine','Planejar roteiro de treinamento operacional sobre {x}'),
  ('routine','Revisar manual de manutenção e documentação de {x}'),
  ('creative','Explorar melhorias de produtividade com menor desperdício em {x}'),
  ('highrisk','Decidir descarte de lote crítico de {x} sem inspeção'),
 ],
 'construction': [
  ('routine','Comparar especificações e memorial descritivo de {x}'),
  ('routine','Montar checklist de compatibilização de projeto de {x}'),
  ('routine','Organizar orçamento preliminar com quantitativos de {x}'),
  ('routine','Criar cronograma e lista de pendências de {x}'),
  ('creative','Propor soluções de layout e materiais para {x}'),
  ('routine','Revisar regulamentos e requisitos locais aplicáveis a {x}'),
  ('highrisk','Validar segurança e conformidade técnica de {x} apenas com IA'),
  ('highrisk','Liberar obra de {x} sem inspeção técnica presencial'),
  ('sensitive','Enviar plantas confidenciais e controles de acesso de {x} à IA pública'),
  ('routine','Preparar relatório fotográfico e registro de não conformidade de {x}'),
  ('learn','Aprender a interpretar desenho técnico e cotas de {x}'),
  ('routine','Organizar documentação de fornecedores e medições de {x}'),
  ('creative','Avaliar alternativas de sustentabilidade e eficiência de {x}'),
  ('highrisk','Autorizar mudança de projeto de {x} sem responsável técnico'),
 ],
 'agro': [
  ('routine','Organizar dados de campo e produtividade de {x}'),
  ('routine','Comparar boletins técnicos e pesquisas sobre {x}'),
  ('routine','Criar calendário de monitoramento de {x}'),
  ('routine','Montar planilha de custos e insumos de {x}'),
  ('creative','Formular hipóteses para queda de produtividade em {x}'),
  ('routine','Interpretar gráficos históricos de clima ligados a {x}'),
  ('highrisk','Decidir aplicação de agrotóxico em {x} apenas por IA'),
  ('highrisk','Definir intervenção sanitária para {x} sem profissional habilitado'),
  ('sensitive','Compartilhar dados contratuais sigilosos de produtores de {x} com IA pública'),
  ('learn','Aprender princípios de manejo de {x} antes de automatizar a análise'),
  ('routine','Criar checklist de inspeção e rastreabilidade de {x}'),
  ('routine','Preparar relatório técnico de observações de campo em {x}'),
  ('creative','Comparar alternativas de manejo regenerativo em {x}'),
  ('routine','Resumir indicadores ambientais relacionados a {x}'),
 ],
 'logistics': [
  ('routine','Planejar rotas e entregas para {x} com restrições reais'),
  ('routine','Consolidar indicadores de prazo e custo de {x}'),
  ('routine','Criar checklist de documentação de {x}'),
  ('routine','Resumir ocorrências e atrasos no processo de {x}'),
  ('creative','Propor melhorias alternativas no fluxo de {x}'),
  ('routine','Analisar padrão de demanda e sazonalidade de {x}'),
  ('highrisk','Liberar viagem ou operação de {x} contrariando verificação de segurança'),
  ('highrisk','Definir rota crítica de {x} sem conferir restrições vigentes'),
  ('sensitive','Compartilhar dados identificáveis de clientes de {x} em IA pública'),
  ('routine','Organizar manutenção, inspeções e certificados de {x}'),
  ('learn','Aprender procedimentos de segurança de {x} em casos simulados'),
  ('routine','Preparar comunicação operacional sobre mudanças de {x}'),
  ('creative','Investigar causas de falhas de atendimento em {x}'),
  ('highrisk','Alterar protocolo de segurança de {x} baseado somente em chatbot'),
 ],
 'hospitality': [
  ('routine','Criar escala de trabalho e checklist diário para {x}'),
  ('routine','Organizar reservas, pedidos e solicitações de {x}'),
  ('routine','Revisar comunicação de atendimento ao público sobre {x}'),
  ('routine','Preparar orientações simples para clientes sobre {x}'),
  ('creative','Criar novas experiências e serviços para {x}'),
  ('routine','Comparar custos, estoque e desperdício de {x}'),
  ('highrisk','Ignorar normas sanitárias ou de segurança em {x} por sugestão da IA'),
  ('sensitive','Enviar dados pessoais de hóspedes ou clientes de {x} a chatbot público'),
  ('routine','Planejar campanha sazonal e divulgação de {x}'),
  ('routine','Elaborar respostas a dúvidas frequentes de {x}'),
  ('learn','Aprender procedimentos técnicos de {x} sem depender de respostas prontas'),
  ('routine','Criar planilha de acompanhamento de satisfação com {x}'),
  ('creative','Explorar alternativas para resolver reclamações sobre {x}'),
  ('highrisk','Alterar uma indicação de segurança alimentar ou sanitária de {x} sem inspeção'),
 ],
 'creativeprof': [
  ('creative','Criar conceito autoral para {x} antes de pedir sugestões a uma IA'),
  ('creative','Explorar três narrativas visuais ou sonoras para {x}'),
  ('routine','Revisar texto, transcrição ou legendas de {x}'),
  ('routine','Organizar referências, licenças e arquivos usados em {x}'),
  ('creative','Desenvolver um storyboard ou roteiro alternativo para {x}'),
  ('routine','Preparar lista de cenas, equipamentos e entregas de {x}'),
  ('learn','Estudar técnicas e experimentar manualmente soluções para {x}'),
  ('highrisk','Publicar conteúdo difamatório ou enganoso ligado a {x} sem checar fatos'),
  ('sensitive','Enviar material sigiloso de cliente de {x} a IA pública sem autorização'),
  ('authorship','Escrever um texto original de {x} com autoria própria e transparência'),
  ('routine','Verificar créditos, direitos autorais e fontes de {x}'),
  ('routine','Criar material de divulgação e descrição acessível de {x}'),
  ('creative','Gerar alternativas de composição sem copiar obras de terceiros em {x}'),
  ('routine','Analisar feedback recebido sobre {x} e categorizar ajustes'),
 ],
 'social': [
  ('routine','Resumir orientações públicas e benefícios disponíveis para {x}'),
  ('routine','Preparar plano de acompanhamento de {x} com avaliação humana'),
  ('routine','Criar comunicação acessível sobre serviços de {x}'),
  ('routine','Organizar agenda de ações e indicadores de {x}'),
  ('creative','Desenvolver abordagens comunitárias para melhorar {x}'),
  ('routine','Mapear programas, editais e fontes oficiais relevantes para {x}'),
  ('highrisk','Definir acesso a benefícios ou acolhimento em {x} só com IA'),
  ('sensitive','Enviar histórico pessoal de pessoas atendidas em {x} para chatbot público'),
  ('routine','Preparar material de capacitação de equipes sobre {x}'),
  ('routine','Criar questionário de satisfação e escuta para {x}'),
  ('learn','Estudar legislação e protocolos básicos de {x} com casos simulados'),
  ('creative','Identificar perguntas pouco exploradas sobre necessidades em {x}'),
  ('routine','Analisar dados agregados e não identificáveis de {x}'),
  ('highrisk','Desconsiderar sinais de perigo em {x} porque a IA tranquilizou'),
 ],
 'personal': [
  ('routine','Comparar informações confiáveis e opções disponíveis de {x}'),
  ('routine','Organizar documentos e perguntas para resolver {x}'),
  ('routine','Criar checklist de etapas e prazos para {x}'),
  ('routine','Entender requisitos e custos antes de contratar serviço de {x}'),
  ('learn','Aprender habilidades básicas para resolver {x} sem depender de IA'),
  ('creative','Pensar em alternativas pessoais para melhorar {x}'),
  ('routine','Comparar alternativas práticas para {x} sem delegar a decisão final'),
  ('sensitive','Enviar documentos pessoais identificáveis sobre {x} para IA pública'),
  ('routine','Preparar perguntas para uma consulta ou reunião sobre {x}'),
  ('routine','Resumir informações recebidas sobre {x} e checar pontos duvidosos'),
  ('routine','Organizar meu acompanhamento pessoal das atividades de {x}'),
  ('routine','Criar plano semanal de atividades relacionado a {x}'),
  ('routine','Identificar quais informações de {x} precisam de confirmação independente'),
  ('routine','Montar orçamento pessoal preliminar para {x}'),
 ],
}

# Perfis ocupacionais e tópicos materiais. O agrupamento é editorial, inspirado
# em famílias O*NET e pesquisas de uso real, não uma amostra aleatória de profissões.
PROFILES = []
def add(archetype, sector, block):
    for line in block.strip().splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        role,values=line.split('|',1)
        topics=[x.strip() for x in values.split(';') if x.strip()]
        if len(topics)<5: raise ValueError(f'{role} tem poucos contextos: {topics}')
        PROFILES.append(dict(profession=role.strip(),sector=sector,archetype=archetype,topics=topics))

add('research','Ciência e pesquisa', '''
Pesquisador biomédico|biomarcadores de sepse; barreira hematoencefálica; imunoterapia contra tumores; organoides humanos; liberação controlada de fármacos; biomateriais implantáveis; marcadores inflamatórios; cicatrização de tecidos
Pesquisador clínico|desfechos de mortalidade hospitalar; desenho de ensaio randomizado; deterioração clínica precoce; eventos adversos de medicamentos; qualidade de vida de pacientes; registros eletrônicos de saúde; aderência ao tratamento; recrutamento de participantes
Doutorando|revisão de literatura da tese; capítulo de métodos quantitativos; análise crítica da discussão; proposta de hipótese central; identificação de lacunas científicas; resposta a revisores; desenho de experimento piloto; estrutura de apresentação de defesa
Mestrando|projeto de dissertação; revisão bibliográfica; metodologia de pesquisa; questionário de coleta de dados; análise de resultados preliminares; apresentação de qualificação; estrutura de manuscrito; planejamento do cronograma acadêmico
Epidemiologista|incidência de doenças infecciosas; análise de coortes populacionais; estudos caso-controle; avaliação de fatores de risco; vieses de seleção; séries temporais de vigilância; indicadores de morbimortalidade; métodos de inferência causal
Bioinformatas|sequenciamento de RNA; variantes genéticas; análise de single-cell RNA-seq; anotação de genomas; análise de proteômica; interpretação de vias moleculares; qualidade de dados ômicos; desenvolvimento de pipelines reprodutíveis
Estatístico acadêmico|modelos de Cox; regressão logística; análise de dados longitudinais; imputação de dados faltantes; poder estatístico; métodos bayesianos; interpretação de causalidade; validação externa de modelos
Cientista de dados em pesquisa|preprocessamento de dados experimentais; validação cruzada; detecção de vazamento de dados; modelagem de séries temporais; calibração de modelos; documentação de pipelines; interpretabilidade de resultados; reprodutibilidade computacional
Pesquisador em química|catálise enzimática; caracterização espectroscópica; síntese de polímeros; reações organometálicas; cinética de reações; estabilidade de formulações; métodos de cromatografia; mecanismos de reação
Cientista de materiais|fadiga de ligas metálicas; polímeros biodegradáveis; materiais para baterias; resistência de cerâmicas; microscopia eletrônica; propriedades térmicas; materiais compósitos; adesão interfacial
Físico experimental|interferometria óptica; calibração de sensores; física de partículas; medições de radiofrequência; propriedades de semicondutores; análise de ruído instrumental; física de baixas temperaturas; métodos de imageamento
Matemático pesquisador|equações diferenciais parciais; teoria dos números; otimização convexa; geometria algébrica; processos estocásticos; sistemas dinâmicos; teoria dos grafos; métodos numéricos
Neurocientista|plasticidade sináptica; circuitos do hipocampo; conectividade cerebral; potenciais evocados; modelos animais de memória; neuroimagem funcional; distúrbios do sono; mecanismos de atenção
Pesquisador ambiental|microplásticos em águas doces; poluição por partículas finas; impactos de ondas de calor; conservação de manguezais; acidificação oceânica; biodiversidade urbana; contaminação do solo; mudanças no regime de chuvas
Cientista social|mobilidade social; desigualdade educacional; comportamento de consumo; participação cívica; entrevistas qualitativas; pesquisa etnográfica; análise de discursos; políticas de habitação
Historiador acadêmico|fontes primárias do século XIX; arquivos jornalísticos; história da saúde pública; registros de imigração; cronologias políticas; história industrial; memória oral; história da ciência
Bibliotecário de pesquisa|estratégias de busca bibliográfica; padronização de referências; curadoria de repositórios; revisão sistemática de estudos; identificação de periódicos predatórios; metadados DOI; gestão de dados FAIR; preservação digital
Técnico de laboratório|registro de experimentos celulares; curvas de calibração; rastreabilidade de reagentes; controle de amostras; procedimentos de biossegurança; manutenção de equipamentos; protocolos de qualidade; preparação de soluções
Coordenador de pesquisa clínica|critérios de elegibilidade; calendário de visitas de estudo; desvio de protocolo; monitoramento de eventos adversos; documentação regulatória; reconciliação de dados; comunicação com centros de pesquisa; proteção de participantes
Pesquisador de políticas públicas|avaliação de programas sociais; evidências sobre habitação; estudo de impacto de políticas; análise de custo-benefício; indicadores educacionais; avaliação de transporte público; participação cidadã; desigualdades regionais
''')
add('clinical','Saúde e assistência', '''
Médico de família|diabetes tipo 2; hipertensão arterial; asma persistente; dor lombar; infecção urinária; prevenção cardiovascular; obesidade; cuidados de saúde mental
Médico emergencista|dor torácica aguda; acidente vascular cerebral; sepse; insuficiência respiratória; traumatismo craniano; choque anafilático; intoxicação medicamentosa; hemorragia digestiva
Cardiologista|insuficiência cardíaca; fibrilação atrial; síndrome coronariana; dislipidemia; hipertensão resistente; valvopatias; risco cardiovascular; reabilitação cardíaca
Oncologista|câncer de pulmão; melanoma; leucemia mieloide aguda; câncer de mama; imunoterapia oncológica; efeitos adversos da quimioterapia; testes moleculares de tumores; cuidados paliativos
Pediatra|febre em lactentes; vacinação infantil; bronquiolite; desenvolvimento neuropsicomotor; alergia alimentar; desidratação; otite média; asma infantil
Radiologista|tomografia de tórax; ressonância de cérebro; radiografia de tórax; ultrassom abdominal; achados incidentais; BI-RADS; protocolos de contraste; qualidade de imagem
Patologista|imuno-histoquímica tumoral; margens cirúrgicas; citologia cervical; histopatologia pulmonar; biópsia gastrointestinal; classificação tumoral; biomarcadores teciduais; laudos anatomopatológicos
Anestesiologista|avaliação pré-anestésica; manejo de via aérea; analgesia perioperatória; bloqueio regional; monitoramento intraoperatório; recuperação pós-anestésica; interações de anestésicos; complicações anestésicas
Cirurgião geral|colecistectomia laparoscópica; hérnias abdominais; apendicite aguda; cuidados pós-operatórios; infecção de sítio cirúrgico; preparo cirúrgico; sangramento pós-operatório; recuperação acelerada
Enfermeiro assistencial|passagem de plantão; prevenção de quedas; cuidado de feridas; administração de medicamentos; sinais vitais alterados; orientações de alta; protocolos de infecção; avaliação de dor
Enfermeiro de UTI|ventilação mecânica; prevenção de delirium; sepse em UTI; lesão por pressão; sedação e analgesia; cateter venoso central; balanço hídrico; mobilização precoce
Farmacêutico clínico|interações medicamentosas; reconciliação medicamentosa; ajuste renal de doses; anticoagulantes; antibióticos de amplo espectro; farmacovigilância; aderência medicamentosa; medicamentos de alta vigilância
Fisioterapeuta|reabilitação pós-AVC; dor lombar crônica; recuperação de cirurgia ortopédica; lesão de ombro; treino de marcha; reabilitação respiratória; retorno ao esporte; dor cervical
Psicólogo clínico|terapia cognitivo-comportamental; transtornos de ansiedade; depressão; avaliação psicológica; manejo de estresse; prevenção de recaídas; psicoeducação; processos de luto
Nutricionista|diabetes e alimentação; desnutrição hospitalar; nutrição enteral; alimentação infantil; síndrome metabólica; doença celíaca; dieta para atleta; transtornos alimentares
Dentista|cárie dentária; doença periodontal; tratamento endodôntico; próteses dentárias; cirurgia de terceiros molares; radiografia odontológica; lesões de mucosa oral; prevenção de infecções
Fonoaudiólogo|disfagia pós-AVC; desenvolvimento da fala; alterações de voz; reabilitação auditiva; linguagem infantil; apraxia de fala; avaliação de deglutição; comunicação alternativa
Terapeuta ocupacional|autonomia após AVC; adaptação de atividades diárias; reabilitação de mão; integração sensorial; acessibilidade doméstica; saúde mental comunitária; retorno ao trabalho; desenvolvimento infantil
Médico veterinário|doença renal em cães; vacinação de gatos; gastroenterite canina; parasitas em animais; urgências veterinárias; dor crônica em pets; zoonoses; bem-estar animal
Gestor hospitalar|tempo de espera no pronto atendimento; ocupação de leitos; segurança do paciente; indicadores de infecção; fluxo de alta; compras hospitalares; escalas de profissionais; qualidade assistencial
Técnico de enfermagem|checagem de sinais vitais; higiene e conforto; administração assistida de medicação; prevenção de lesões por pressão; mobilização de pacientes; identificação segura; cuidados com cateteres; registro de cuidados
Médico de saúde pública|campanhas de vacinação; rastreamento de doenças; vigilância epidemiológica; saúde de populações vulneráveis; comunicação de risco; indicadores de atenção primária; prevenção de arboviroses; programas de saúde comunitária
Profissional de laboratório clínico|controle de qualidade de hemograma; resultados bioquímicos; triagem de amostras; microbiologia clínica; rastreabilidade de resultados; critérios de rejeição de amostras; interpretação de flags laboratoriais; validação de equipamentos
''')
add('engineering','Engenharia', '''
Engenheiro civil|dimensionamento de fundações; cálculo de vigas; drenagem urbana; pavimentos rodoviários; contenção de encostas; projeto de concreto armado; estruturas de pontes; estabilidade de taludes
Engenheiro estrutural|análise de cargas sísmicas; flambagem de pilares; conexão de estruturas metálicas; fadiga estrutural; esforços em treliças; reforço de lajes; verificação de flechas; ancoragens de concreto
Engenheiro elétrico|proteção de circuitos; dimensionamento de transformadores; análise de harmônicas; redes de média tensão; aterramento elétrico; quadros de distribuição; instalações fotovoltaicas; coordenação de disjuntores
Engenheiro mecânico|trocadores de calor; dimensionamento de eixos; vibração de equipamentos; transmissões mecânicas; sistemas de refrigeração; fadiga de componentes; dinâmica de fluidos; análise térmica de motores
Engenheiro biomédico|dispositivos médicos implantáveis; monitoramento de sinais vitais; sensores vestíveis; ensaios de biocompatibilidade; processamento de sinais ECG; segurança elétrica médica; validação de software clínico; dispositivos microfluídicos
Engenheiro químico|balanço de massa; reatores químicos; destilação fracionada; tratamento de efluentes; controle de pH industrial; transferência de calor; segurança de processos; cristalização de produtos
Engenheiro de materiais|análise metalográfica; ensaio de tração; compósitos poliméricos; corrosão de ligas; tratamento térmico; adesivos industriais; caracterização de revestimentos; fratura de materiais
Engenheiro aeronáutico|aerodinâmica de asa; vibração de fuselagem; sistemas hidráulicos de aeronaves; análise de confiabilidade; controle de voo; fadiga de componentes aéreos; manutenção preditiva; materiais aeroespaciais
Engenheiro ambiental|estação de tratamento de água; inventário de emissões; qualidade do ar; análise de impactos ambientais; remediação de solo; gestão de resíduos; monitoramento de rios; licenciamento ambiental
Engenheiro de produção|balanceamento de linha; indicadores OEE; gestão de estoque; análise de gargalos; planejamento de capacidade; melhoria contínua; simulação de filas; layout fabril
Engenheiro de automação|controladores PLC; sensores industriais; redes Modbus; sistemas SCADA; atuadores hidráulicos; lógica de intertravamento; robôs colaborativos; controle de temperatura
Engenheiro de telecomunicações|cobertura de redes 5G; fibra óptica; interferência de RF; antenas setoriais; protocolos IP; latência de redes; infraestrutura de datacenter; enlaces de rádio
Engenheiro geotécnico|sondagens SPT; capacidade de carga do solo; estabilidade de barragens; ensaios triaxiais; recalque de fundações; contenções com tirantes; infiltração em solos; análise de liquefação
Engenheiro de energia|projeto de microgeração solar; armazenamento em baterias; análise de demanda elétrica; integração de eólica; eficiência energética predial; resposta à demanda; subestações; previsão de geração
Engenheiro de transporte|simulação de tráfego; tempo de semáforos; demanda de ônibus; acessibilidade viária; segurança rodoviária; planejamento cicloviário; corredores de ônibus; gestão de interseções
Engenheiro de segurança do trabalho|análise preliminar de risco; investigação de quase acidentes; proteção de máquinas; entrada em espaço confinado; gestão de EPIs; controle de incêndio; trabalho em altura; exposição ocupacional
Engenheiro naval|estabilidade de embarcações; resistência de casco; sistemas de propulsão; proteção anticorrosiva; válvulas marítimas; sistemas de lastro; vibração naval; consumo de combustível
Engenheiro de petróleo|integridade de poços; sistemas de bombeio; corrosão em dutos; medição de vazão; separação óleo-água; controle de pressão; perfuração direcional; gerenciamento de reservatórios
''')
add('software','Tecnologia e dados', '''
Desenvolvedor backend|autenticação em API; filas de mensagens; transações SQL; cache distribuído; paginação de endpoints; serviços de pagamento; logs estruturados; controle de concorrência
Desenvolvedor frontend|componentes React; acessibilidade WCAG; formulários complexos; renderização no navegador; CSS responsivo; otimização de Core Web Vitals; estado compartilhado; testes de interface
Desenvolvedor mobile|sincronização offline; notificações push; armazenamento local; permissões de câmera; desempenho em Android; layouts em iOS; testes de interface móvel; autenticação biométrica
Engenheiro DevOps|pipeline de CI/CD; infraestrutura como código; deploy em Kubernetes; monitoramento Prometheus; rollback de serviço; gerenciamento de secrets; imagens de contêiner; alertas de observabilidade
Engenheiro SRE|latência de API; incidentes de disponibilidade; orçamento de erro SLO; saturação de servidores; análise pós-incidente; autoescalonamento; métricas RED; recuperação de desastre
Analista de cibersegurança|revisão de logs de autenticação; políticas MFA; auditoria de dependências; análise de phishing; controle de acesso; resposta a incidentes; hardening de servidores; classificação de vulnerabilidades
Administrador de bancos de dados|índices PostgreSQL; replicação de dados; planos de execução SQL; backups de banco; integridade referencial; particionamento; recuperação point-in-time; migrações de esquema
Cientista de dados|previsão de churn; modelos de classificação; detecção de anomalias; análise de coortes; previsão de demanda; segmentação de clientes; explicabilidade de modelos; testes A/B
Engenheiro de dados|pipelines ETL; ingestão de eventos; qualidade de dados; data lake; orquestração Airflow; governança de esquemas; tabelas particionadas; monitoramento de jobs
Engenheiro de IA|avaliação de RAG; qualidade de embeddings; proteção contra prompt injection; avaliação de respostas; pipelines de inferência; monitoramento de drift; classificação de documentos; agentes de ferramentas
Analista de qualidade de software|testes E2E; cenários de regressão; matriz de cobertura; testes de API; dados sintéticos de teste; gestão de bugs; critérios de aceite; automação Playwright
Designer de experiência UX|pesquisa com usuários; mapa de jornadas; design system; protótipos de onboarding; testes de usabilidade; arquitetura da informação; acessibilidade digital; métricas de conversão
Gerente de produto digital|priorização de backlog; pesquisa de concorrência; entrevistas com usuários; definição de métricas; planejamento de roadmap; requisitos de feature; análise de retenção; estratégia de lançamento
Arquiteto de soluções em nuvem|arquitetura multi-região; segregação de redes; custo de serviços cloud; balanceamento de carga; migração de serviços; observabilidade de infraestrutura; IAM; segurança de dados
Analista de BI|indicadores de vendas; DAX no Power BI; modelos dimensionais; dashboards executivos; SQL analítico; qualidade de KPIs; métricas de retenção; custos operacionais
Analista de suporte técnico|incidentes de login; configuração de VPN; falhas de impressoras; recuperação de arquivos; atualização de software; permissões de usuários; triagem de tickets; diagnóstico de rede
Especialista em GIS|geocodificação de endereços; sensoriamento remoto; análise de cobertura vegetal; mapas de acessibilidade; imagens de satélite; projeções cartográficas; modelos de elevação; análise espacial
''')
add('education','Educação', '''
Professor de educação infantil|alfabetização inicial; desenvolvimento da linguagem; contação de histórias; atividades sensoriais; coordenação motora; brincadeiras colaborativas; comunicação com famílias; rotina de acolhimento
Professor do ensino fundamental|frações e porcentagens; ecossistemas brasileiros; leitura e interpretação; história do Brasil; redação argumentativa; geometria; educação financeira básica; interpretação de gráficos
Professor do ensino médio|funções exponenciais; genética mendeliana; eletromagnetismo; química orgânica; literatura brasileira; sociologia contemporânea; redação ENEM; probabilidade
Professor universitário|aula de estatística; seminário de metodologia; revisão de bioética; avaliação de projetos; cálculo avançado; laboratório de engenharia; pesquisa orientada; letramento científico
Professor de idiomas|conversação em inglês; escrita acadêmica em espanhol; gramática portuguesa; pronúncia do francês; leitura de textos técnicos; compreensão auditiva; vocabulário profissional; preparação para proficiência
Professor de educação especial|material de leitura acessível; comunicação alternativa; inclusão em sala de aula; adaptação de avaliação; apoio a dislexia; apoio a deficiência visual; planos individualizados; desenvolvimento de autonomia
Coordenador pedagógico|acompanhamento de aprendizagem; formação de professores; planejamento bimestral; avaliação institucional; revisão de currículo; recuperação paralela; comunicação com responsáveis; gestão de indicadores escolares
Diretor escolar|gestão de matrículas; política de frequência; segurança escolar; contratação de docentes; gestão de orçamento; comunicação de crises; planejamento de eventos; avaliação de desempenho escolar
Tutor de reforço escolar|equações de primeiro grau; escrita de redação; interpretação de texto; operações com frações; fundamentos de física; química básica; geometria plana; hábitos de estudo
Designer instrucional|curso de integração de funcionários; treinamento de segurança; módulo de liderança; oficina de atendimento; curso técnico online; avaliação de competências; trilha de aprendizagem; produção de aulas digitais
''')
add('legal','Direito e regulação', '''
Advogado cível|responsabilidade civil; indenização por danos; contratos de prestação de serviço; direito de família; conflito condominial; obrigações contratuais; execução de sentença; ações possessórias
Advogado trabalhista|rescisão contratual; jornada de trabalho; assédio no trabalho; verbas rescisórias; estabilidade de emprego; acordo coletivo; processo trabalhista; acidente de trabalho
Advogado tributarista|planejamento tributário; tributação de serviços; recuperação de créditos fiscais; ICMS; ISS; imposto de renda empresarial; contencioso tributário; obrigações acessórias
Advogado criminalista|direito de defesa; medidas cautelares; processo penal; prova testemunhal; cadeia de custódia; investigação criminal; recurso de apelação; garantias constitucionais
Advogado de proteção de dados|LGPD; consentimento informado; transferências internacionais de dados; resposta a incidente de vazamento; contratos com operadores; relatório de impacto; anonimização; política de retenção
Analista de compliance|prevenção à lavagem de dinheiro; política anticorrupção; due diligence de fornecedores; conflito de interesses; canal de denúncias; controles internos; prevenção de fraudes; auditoria regulatória
Servidor público|processo administrativo; atendimento ao cidadão; transparência ativa; compras públicas; tramitação de requerimentos; arquivo administrativo; prestação de contas; comunicação institucional
Gestor de licitações|edital de contratação; pesquisa de preços; análise de propostas; termo de referência; fiscalização contratual; requisitos de habilitação; gestão de riscos de compras; recursos administrativos
Assistente jurídico|organização de processos; preparação de petições; controle de prazos; catalogação de documentos; acompanhamento de audiências; correspondência jurídica; revisão de contratos; pesquisa de precedentes
Analista regulatório|registro de produtos; requisitos de rotulagem; normas de segurança; mudanças regulatórias; rastreabilidade de documentação; fiscalização de conformidade; boas práticas de fabricação; auditorias regulatórias
Auditor público|prestação de contas; execução orçamentária; contratos públicos; risco de fraude; indicadores de eficiência; integridade de compras; conformidade fiscal; gestão patrimonial
Defensor público|acesso a benefícios; orientação criminal; conflito familiar; proteção de crianças; medidas protetivas; direito à moradia; execução penal; atendimento a populações vulneráveis
''')
add('finance','Finanças e contabilidade', '''
Contador|fechamento contábil; conciliação bancária; classificação fiscal; despesas operacionais; demonstração de resultados; obrigações acessórias; folha de pagamento; notas fiscais
Auditor independente|testes de controle interno; evidências de auditoria; amostragem contábil; notas explicativas; fraude contábil; saldos de estoque; contas a receber; conformidade financeira
Analista financeiro|fluxo de caixa; projeção de receitas; análise de margem; orçamento anual; KPIs financeiros; alocação de capital; análise de custos; avaliação de investimentos
Controller|fechamento mensal; variações orçamentárias; planejamento de custos; relatórios gerenciais; centros de custos; orçamento consolidado; indicadores de rentabilidade; compliance financeiro
Consultor de investimentos|alocação de portfólio; fundos de índice; planejamento de aposentadoria; títulos de renda fixa; análise de risco; tributação de investimentos; diversificação de ativos; perfil de investidor
Atuário|cálculo de reservas; precificação de seguros; modelos de sinistralidade; provisões matemáticas; análise de longevidade; modelagem de riscos; projeções demográficas; solvência
Analista de crédito|capacidade de pagamento; histórico de inadimplência; score de crédito; avaliação de garantias; risco de contraparte; concessão de empréstimos; renegociação de dívidas; carteira de recebíveis
Analista de tesouraria|posição de caixa; hedge cambial; contas bancárias; pagamentos a fornecedores; alocação de liquidez; previsão de necessidades de caixa; conciliação financeira; riscos de taxa de juros
Especialista tributário|declaração de imposto de renda; apuração de tributos; obrigações fiscais; interpretação de norma tributária; documentação de incentivos; cálculo de créditos fiscais; regimes tributários; auditoria fiscal
Gestor de seguros|sinistros de automóveis; cobertura residencial; avaliação de apólices; precificação de risco; renovação de contratos; reclamações de segurados; fraude em sinistros; documentos de indenização
''')
add('business','Gestão e operações', '''
Gerente de projetos|cronograma de entregas; matriz de responsabilidades; análise de riscos; retrospectiva de sprint; acompanhamento de orçamento; status report; gestão de fornecedores; priorização de demandas
Analista de recursos humanos|descrições de vagas; integração de novos funcionários; avaliação de treinamento; políticas internas; pesquisa de clima; folha de pagamento; plano de desenvolvimento; calendário de férias
Recrutador|descrição de cargo; triagem de currículos; entrevista estruturada; comunicação com candidatos; planejamento de contratação; comparação de competências; acompanhamento de vagas; onboarding
Assistente administrativo|relatórios de despesas; atas de reunião; gestão de agendas; organização documental; cadastro de fornecedores; controle de estoque; respostas a e-mails; preparação de eventos
Consultor de gestão|diagnóstico operacional; mapa de processos; plano de transformação; governança de projetos; indicadores de eficiência; desenho organizacional; gestão de mudança; análise de mercado
Gerente de atendimento ao cliente|base de conhecimento; triagem de tickets; redução de espera; análise de reclamações; scripts de suporte; indicadores CSAT; respostas de atendimento; treinamento de equipes
Especialista de compras|comparação de cotações; avaliação de fornecedores; contratos de suprimentos; pedidos de compra; negociação de prazos; categorização de despesas; riscos de abastecimento; compliance de compras
Gerente de operações|demanda de recursos; processos internos; metas de produtividade; fluxo de trabalho; planejamento trimestral; indicadores de qualidade; expansão operacional; análise de gargalos
Analista de negócios|levantamento de requisitos; mapeamento de jornadas; análise de stakeholders; definição de métricas; avaliação de processos; plano de ação; impacto de mudança; elaboração de casos de negócio
Consultor de carreira|currículo para vaga de tecnologia; preparação para entrevista; transição de carreira; planejamento de portfólio; networking profissional; pesquisa salarial; negociação de oferta; atualização de LinkedIn
Especialista em qualidade|análise de não conformidades; auditoria ISO; procedimentos operacionais; indicadores de defeitos; ações corretivas CAPA; rastreabilidade de registros; avaliação de fornecedores; melhoria de processos
''')
add('marketing','Marketing, mídia e vendas', '''
Jornalista|checagem de declarações públicas; entrevista com especialista; apuração de notícias; contexto de dados econômicos; investigação de fontes; pauta de reportagem; edição de matéria; divulgação de resultados científicos
Divulgador científico|roteiro de vídeo baseado em paper; revisão de referências DOI; simplificação de resultado clínico; checagem de afirmação viral; explicação de método científico; carrossel educativo; entrevista com pesquisador; tradução de termos técnicos
Criador de conteúdo|ideias para Reels; roteiro de YouTube; calendário semanal de vídeos; análise de engajamento; legendas acessíveis; série educativa; pesquisa de tendências; edição de newsletter
Redator publicitário|copy de landing page; campanha de lançamento; anúncios para buscadores; e-mail de conversão; posicionamento de marca; textos para catálogo; sequência de onboarding; teste de mensagens
Gestor de redes sociais|relatório do Instagram; conteúdo para LinkedIn; respostas a comentários; calendário de posts; métricas de audiência; campanha de TikTok; planejamento de comunidade; diretrizes de tom de voz
Especialista em SEO|intenção de busca; estrutura de páginas; pesquisa de palavras-chave; auditoria de conteúdo; metadados; SEO local; estratégia de links; páginas de produto
Gerente de marketing|lançamento de serviço; segmentação de audiência; campanha multicanal; pesquisa de mercado; relatório de CAC; posicionamento de produto; comunicação de marca; análise de funil
Vendedor B2B|prospecção de clientes; proposta comercial; respostas a objeções; planejamento de contas; preparação de demonstração; CRM; negociação de renovação; previsão de vendas
Gestor de comércio eletrônico|descrição de produtos; recuperação de carrinho; avaliações de consumidores; categorias de catálogo; estratégia de promoção; anúncios de marketplace; análise de conversão; atendimento de devoluções
Assessor de imprensa|release de pesquisa; posicionamento institucional; contatos de jornalistas; perguntas para coletiva; nota de esclarecimento; gestão de crise; briefing de porta-voz; monitoramento de mídia
Especialista em comunicação interna|comunicado de mudanças; pesquisa de engajamento; newsletter corporativa; manual de integração; campanha de segurança; eventos internos; FAQ de benefícios; comunicação de liderança
''')
add('manufacture','Indústria e manufatura', '''
Gestor de fábrica|produção por turno; tempo de parada; indicadores OEE; consumo de matérias-primas; produtividade de células; manutenção programada; segurança industrial; descarte de resíduos
Operador de máquina CNC|programação de peça CNC; tolerâncias de usinagem; troca de ferramentas; inspeção dimensional; setup de máquina; programa G-code; controle de refugo; ajuste de velocidade de corte
Técnico de manutenção industrial|rolamentos de motores; bombas centrífugas; painéis elétricos; compressores; sistemas pneumáticos; sensores de temperatura; redutores mecânicos; manutenção preditiva
Inspetor de qualidade|inspeção por amostragem; controle dimensional; medição de rugosidade; verificação de lotes; rastreabilidade de produtos; registros de não conformidade; auditorias internas; ensaios não destrutivos
Técnico de alimentos|controle microbiológico; análise de validade; limpeza de linhas; processos HACCP; verificação de temperatura; controle de alérgenos; rotulagem de produtos; rastreabilidade alimentar
Operador de logística industrial|separação de materiais; inventário de peças; recebimento de insumos; abastecimento de linha; movimentação de paletes; conferência de pedidos; controle de validade; comunicação de ocorrências
Soldador industrial|soldagem TIG; soldagem MIG; inspeção de cordões; preparação de juntas; procedimentos WPS; controle de deformação; equipamentos de soldagem; segurança na soldagem
''')
add('construction','Arquitetura e construção', '''
Arquiteto|projeto de residência; reforma de apartamento; acessibilidade em edifícios; iluminação natural; ventilação cruzada; compatibilização de plantas; desenho de fachada; especificação de acabamentos
Urbanista|plano diretor; calçadas acessíveis; corredores de ônibus; uso misto do solo; parques urbanos; drenagem de bairros; habitação popular; mobilidade a pé
Gerente de obra|cronograma de fundações; medições de serviços; entrega de materiais; compatibilização de projetos; inspeção de concretagem; controle de segurança; gestão de equipes; relatório de progresso
Mestre de obras|execução de alvenaria; impermeabilização de laje; instalação hidráulica; aplicação de revestimento; concretagem de pilares; regularização de piso; montagem de formas; inspeção de andaimes
Topógrafo|levantamento planialtimétrico; georreferenciamento rural; locação de obra; curvas de nível; nivelamento de terreno; implantação de vias; controle de marcos; levantamento cadastral
Designer de interiores|layout de cozinha; ergonomia em escritório; iluminação de sala; projeto de marcenaria; escolha de acabamentos; mobiliário adaptado; acessibilidade residencial; organização de espaços
Orçamentista de obras|quantitativo de concreto; orçamento de instalações; custo de mão de obra; composição de preços unitários; reajuste de contrato; comparação de propostas; cronograma físico-financeiro; orçamento de reforma
''')
add('agro','Agro e meio ambiente', '''
Agrônomo|manejo de soja; pragas em milho; fertilidade do solo; irrigação de café; manejo de cana-de-açúcar; análise foliar; agricultura de precisão; controle de doenças de plantas
Agricultor familiar|produção de hortaliças; calendário de plantio; armazenamento de sementes; irrigação de pequena propriedade; comercialização local; controle de custos; manejo de solo; previsão de colheita
Pecuarista|nutrição de bovinos; calendário vacinal de rebanho; controle de parasitas; manejo de pastagens; rastreabilidade animal; gestão de custos; bem-estar animal; reprodução assistida
Engenheiro florestal|inventário de árvores; recuperação de mata ciliar; combate a incêndios florestais; silvicultura; geoprocessamento florestal; licenciamento de manejo; monitoramento de biodiversidade; áreas de preservação
Biólogo da conservação|monitoramento de espécies ameaçadas; fragmentação de habitat; ecologia de polinizadores; restauração de recifes; invasões biológicas; corredores ecológicos; educação ambiental; monitoramento de fauna
Técnico em irrigação|gotejamento agrícola; cálculo de vazão; manutenção de bombas; sensores de umidade; uniformidade de irrigação; consumo de água; fertirrigação; drenagem de campo
Gestor de resíduos|coleta seletiva; resíduos hospitalares; reciclagem industrial; compostagem municipal; logística reversa; inventário de resíduos; gestão de aterros; destinação de perigosos
Meteorologista|previsão de chuva intensa; ondas de calor; dados de estações meteorológicas; avisos de tempestade; modelos climáticos; variabilidade sazonal; monitoramento de seca; impactos de geadas
''')
add('logistics','Transporte e logística', '''
Gestor de logística|roteirização urbana; transporte refrigerado; entrega de última milha; distribuição regional; transferência entre centros; movimentação de carga; planejamento de capacidade; operação portuária
Motorista profissional|entregas rodoviárias; verificação pré-viagem; documentação de carga; pausas e descanso; condições de estrada; manutenção de caminhão; registro de incidentes; cronograma de entrega
Gestor de frota|revisão preventiva; consumo de combustível; rastreamento de veículos; sinistros de trânsito; escala de motoristas; renovação de frota; telemetria veicular; gestão de pneus
Agente de viagens|roteiro de férias; tarifas aéreas; regras de bagagem; requisitos de visto; hotéis acessíveis; planejamento de conexões; seguro viagem; cancelamento de reservas
Piloto comercial|plano de voo; briefing meteorológico; lista de verificação; gerenciamento de combustível; regras de espaço aéreo; comunicação com controle; documentação técnica; planejamento de alternados
Despachante aduaneiro|classificação fiscal de importações; documentação de exportação; conferência de faturas; desembaraço aduaneiro; certificados de origem; regimes especiais; requisitos sanitários; cálculo de tarifas
Supervisor de armazém|layout de picking; inventário rotativo; processamento de pedidos; recebimento de cargas; controle de perdas; gestão de turnos; rastreabilidade de pacotes; segurança de empilhadeiras
Coordenador de transportes públicos|linhas de ônibus; pontualidade de frota; distribuição de demanda; fiscalização de itinerários; informação ao passageiro; acessibilidade de paradas; planejamento de linhas; operação em dias de evento
''')
add('hospitality','Comércio e serviços', '''
Gerente de restaurante|reservas de mesas; fluxo de cozinha; cardápio sazonal; estoque de alimentos; atendimento a reclamações; controle de desperdício; escala de garçons; segurança alimentar
Chef de cozinha|planejamento de menu; ficha técnica de receita; armazenamento de ingredientes; controle de alergênicos; aproveitamento integral; inventário de cozinha; treinamento de equipe; custos de porção
Confeiteiro|encomendas de bolos; produção de massas; decoração de doces; controle de validade; logística de entrega; alergênicos em confeitaria; precificação de produtos; compras de insumos
Barista|fluxo de pedidos; manutenção de máquina de espresso; cardápio de cafés; treinamento de equipe; estoque de grãos; atendimento a clientes; receita de bebidas; controle de desperdício
Gerente de hotel|reservas de quartos; check-in de hóspedes; housekeeping; gestão de tarifas; reclamações de clientes; manutenção predial; ocupação sazonal; treinamento de recepção
Recepcionista de clínica|agendamento de consultas; orientação pré-exame; remarcação de atendimentos; dúvidas de convênio; controle de salas; confirmação de horários; fluxo de recepção; acessibilidade para pacientes
Vendedor varejista|descrição de produto; atendimento de clientes; política de trocas; promoções sazonais; controle de estoque; vitrine de loja; lançamento de coleção; análise de vendas
Gerente de supermercado|ruptura de estoque; validade de perecíveis; escalas de caixa; inventário de gôndola; reposição de produtos; quebras operacionais; campanhas de preço; atendimento de reclamações
Cabeleireiro|agenda de salão; estoque de tinturas; biossegurança em salão; consulta de estilo; programa de fidelidade; precificação de serviços; treinamento de assistentes; divulgação de cortes
Eletricista residencial|quadro elétrico doméstico; disjuntor desarmando; instalação de tomadas; aterramento de residência; iluminação de cozinha; manutenção de circuitos; orçamento de serviço; relatório de vistoria
Encanador|vazamento em tubulação; manutenção de caixa d’água; pressão hidráulica; instalação de torneiras; desentupimento seguro; peças e conexões; orçamento hidráulico; inspeção preventiva
Mecânico automotivo|falha de ignição; consumo de combustível; sistema de freios; manutenção de suspensão; diagnóstico OBD; troca de óleo; vibração automotiva; orçamento de reparo
''')
add('creativeprof','Cultura e produção criativa', '''
Roteirista|roteiro de documentário; série de ficção; vídeo educativo; filme independente; entrevista narrativa; episódio de podcast; storytelling institucional; curta-metragem
Designer gráfico|identidade de marca; infográfico científico; design de embalagem; cartaz de evento; editorial de revista; ilustração de produto; apresentação institucional; material de campanha
Editor de vídeo|edição de documentário; cortes para Reels; vídeo de treinamento; entrevista multicâmera; legendas de YouTube; trailer de filme; vídeo corporativo; adaptação vertical
Fotógrafo|ensaio de produto; evento corporativo; retrato profissional; cobertura jornalística; fotografia de arquitetura; fotografia de natureza; portfólio comercial; organização de acervo
Ilustrador|livro didático; ilustração científica; personagem de HQ; capa editorial; cartilha de saúde; storyboard; infográfico animado; identidade de jogo
Produtor audiovisual|pré-produção de documentário; planejamento de filmagem; orçamento de vídeo; produção de podcast; gravação externa; captação de áudio; equipe de pós-produção; entrega de campanha
Designer de jogos|mecânicas de puzzle; balanceamento de personagens; missões secundárias; interface de jogo; narrativa interativa; testes com jogadores; sistema de progressão; acessibilidade em games
Editor de livros|revisão de original; preparação de manuscrito; projeto editorial; avaliação de sinopse; organização de capítulos; padronização de notas; planejamento de lançamento; edição de coletânea
Músico e compositor|composição autoral; ensaio de banda; gravação de demo; produção de álbum; apresentação ao vivo; divulgação de show; arranjo original; identidade artística
''')
add('social','Serviço social e organizações', '''
Assistente social|acolhimento familiar; acesso ao CadÚnico; rede de proteção; direitos de idosos; inclusão de pessoas com deficiência; assistência a migrantes; proteção de crianças; encaminhamento habitacional
Gestor de ONG|captação de recursos; relatório de impacto; campanha de doação; prestação de contas; gestão de voluntários; avaliação de projeto social; atendimento comunitário; indicadores sociais
Agente comunitário de saúde|visitas domiciliares; vacinação comunitária; acompanhamento de gestantes; prevenção de dengue; orientação a idosos; busca ativa; educação em saúde; comunicação com equipes
Mediador comunitário|conflitos de vizinhança; assembleias comunitárias; encaminhamento a serviços; diálogo intercultural; ações de bairro; participação cidadã; prevenção de violência; resolução de disputas
Gestor de políticas sociais|programas de inclusão; proteção de renda; acessibilidade urbana; programas de juventude; assistência a idosos; prevenção de violência; acompanhamento escolar; combate à insegurança alimentar
''')
add('personal','Vida cotidiana', '''
Pessoa buscando emprego|comparação de vagas; elaboração de currículo; preparação para entrevista; negociação de salário; organização de candidaturas; pesquisa de empresas; capacitação profissional; transição de carreira
Estudante universitário|resolução de problemas de cálculo; leitura de artigo acadêmico; apresentação de seminário; revisão para prova; escrita de trabalho acadêmico; organização de estudos; exercícios de programação; redação de relatório
Pai ou mãe|rotina de sono infantil; comunicação com escola; escolha de creche; organização de refeições; vacinação familiar; passeios com crianças; planejamento de férias; organização de despesas
Cuidador familiar|agenda de consultas; lista de medicamentos; organização de cuidados; documentação de serviços; adaptação da casa; transporte a consultas; orientações de alta; comunicação com familiares
Pessoa que trabalha remotamente|organização do calendário; reunião virtual; comunicação assíncrona; priorização de tarefas; planejamento de metas; gestão de interrupções; apresentações online; acompanhamento de entregas
Pessoa planejando viagem|comparação de hospedagens; roteiro de cidade; documentação de viagem; orçamento de viagem; transporte local; acessibilidade de atrações; seguro viagem; transporte entre cidades
Microempreendedor individual|emissão de nota fiscal; controle de recebimentos; precificação de serviço; publicação em rede social; atendimento ao cliente; declaração anual; fluxo de caixa; proposta comercial
Consumidor|comparação de notebooks; escolha de plano de internet; compra de eletrodoméstico; comparação de seguros; direitos de garantia; contrato de aluguel; compras de supermercado; planejamento de assinatura
Pessoa organizando finanças pessoais|orçamento familiar; reserva de emergência; dívidas de cartão; metas de poupança; comparação de tarifas; contas mensais; planejamento de aposentadoria; imposto de renda
Pessoa cuidando da casa|orçamento de reforma; manutenção de geladeira; vazamento doméstico; limpeza de ambientes; consumo de energia; organização de despensa; escolha de prestador; redução de desperdício
''')

# Tarefas âncora de alta relevância. Serão os melhores resultados das pesquisas mais comuns.
ANCHORS = [
 ('Escrever minha tese de doutorado', 'authorship','Doutorando','Ciência e pesquisa','academic'),
 ('Escrever minha dissertação de mestrado', 'authorship','Mestrando','Ciência e pesquisa','academic'),
 ('Escrever a discussão de um artigo científico', 'authorship','Pesquisador biomédico','Ciência e pesquisa','academic'),
 ('Escrever a introdução da minha tese', 'authorship','Doutorando','Ciência e pesquisa','academic'),
 ('Revisar a gramática de um artigo científico sem alterar dados', 'routine','Pesquisador biomédico','Ciência e pesquisa','research'),
 ('Buscar artigos científicos no PubMed e verificar os DOI', 'routine','Pesquisador biomédico','Ciência e pesquisa','research'),
 ('Fazer revisão bibliográfica para minha tese', 'routine','Doutorando','Ciência e pesquisa','research'),
 ('Comparar resultados e limitações de ensaios clínicos', 'routine','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Criar hipóteses originais para um projeto de pesquisa', 'creative','Pesquisador biomédico','Ciência e pesquisa','research'),
 ('Definir a pergunta de pesquisa da minha tese', 'creative','Doutorando','Ciência e pesquisa','research'),
 ('Planejar a metodologia de uma pesquisa científica', 'creative','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Criar roteiro de análise estatística no R', 'routine','Estatístico acadêmico','Ciência e pesquisa','research'),
 ('Verificar se referências científicas existem ou foram inventadas', 'routine','Bibliotecário de pesquisa','Ciência e pesquisa','research'),
 ('Escrever resposta aos revisores de um artigo', 'authorship','Pesquisador clínico','Ciência e pesquisa','academic'),
 ('Preparar submissão de projeto ao comitê de ética', 'highrisk','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Ler e entender um artigo científico difícil', 'learn','Estudante universitário','Vida cotidiana','personal'),
 ('Interpretar um intervalo de confiança e um valor de p', 'learn','Estatístico acadêmico','Ciência e pesquisa','research'),
 ('Estudar epidemiologia para uma prova sem receber respostas prontas', 'learn','Mestrando','Ciência e pesquisa','research'),
 ('Resumir guideline médico para discussão clínica', 'routine','Médico de família','Saúde e assistência','clinical'),
 ('Pesquisar evidências científicas sobre tratamento de diabetes', 'routine','Médico de família','Saúde e assistência','clinical'),
 ('Escrever evolução médica a partir de notas clínicas', 'sensitive','Médico de família','Saúde e assistência','clinical'),
 ('Resumir prontuário com dados identificáveis em chatbot público', 'sensitive','Médico de família','Saúde e assistência','clinical'),
 ('Redigir instruções de alta hospitalar com revisão médica', 'routine','Médico emergencista','Saúde e assistência','clinical'),
 ('Decidir diagnóstico médico usando somente ChatGPT', 'highrisk','Médico de família','Saúde e assistência','clinical'),
 ('Interpretar um eletrocardiograma para decidir tratamento', 'highrisk','Cardiologista','Saúde e assistência','clinical'),
 ('Apoiar leitura de ressonância magnética com revisão de radiologista', 'highrisk','Radiologista','Saúde e assistência','clinical'),
 ('Revisar artigos recentes sobre tratamento oncológico', 'routine','Oncologista','Saúde e assistência','clinical'),
 ('Criar material de educação para pacientes sobre hipertensão', 'routine','Enfermeiro assistencial','Saúde e assistência','clinical'),
 ('Resumir literatura sobre segurança de medicamentos', 'routine','Farmacêutico clínico','Saúde e assistência','clinical'),
 ('Buscar diagnósticos diferenciais para caso clínico simulado', 'learn','Médico emergencista','Saúde e assistência','clinical'),
 ('Gerar código Python para analisar dados experimentais', 'routine','Engenheiro biomédico','Engenharia','engineering'),
 ('Analisar sinais de ECG e SpO2 de dispositivos vestíveis', 'routine','Engenheiro biomédico','Engenharia','engineering'),
 ('Dimensionar uma viga estrutural e conferir normas técnicas', 'highrisk','Engenheiro estrutural','Engenharia','engineering'),
 ('Revisar projeto de instalação elétrica residencial', 'highrisk','Engenheiro elétrico','Engenharia','engineering'),
 ('Criar memorial descritivo de uma obra', 'routine','Engenheiro civil','Engenharia','engineering'),
 ('Revisar desenho técnico CAD de um dispositivo médico', 'routine','Engenheiro biomédico','Engenharia','engineering'),
 ('Depurar código Python com um erro de execução', 'routine','Desenvolvedor backend','Tecnologia e dados','software'),
 ('Criar testes unitários para uma API', 'routine','Desenvolvedor backend','Tecnologia e dados','software'),
 ('Aprender a programar do zero sem copiar respostas', 'learn','Desenvolvedor backend','Tecnologia e dados','software'),
 ('Revisar segurança de código antes de fazer deploy', 'highrisk','Analista de cibersegurança','Tecnologia e dados','software'),
 ('Criar um site responsivo em HTML e CSS', 'routine','Desenvolvedor frontend','Tecnologia e dados','software'),
 ('Preparar aulas e exercícios diferenciados para os alunos', 'routine','Professor do ensino fundamental','Educação','education'),
 ('Corrigir prova e atribuir nota automática sem revisão', 'highrisk','Professor do ensino médio','Educação','education'),
 ('Resolver prova individual quando o uso de IA é proibido', 'noai','Estudante universitário','Vida cotidiana','education'),
 ('Pesquisar jurisprudência para um processo', 'routine','Advogado cível','Direito e regulação','legal'),
 ('Escrever minuta de contrato com revisão jurídica', 'authorship','Advogado cível','Direito e regulação','legal'),
 ('Decidir uma ação judicial sem consultar advogado', 'highrisk','Advogado cível','Direito e regulação','legal'),
 ('Organizar planilha de despesas pessoais', 'routine','Pessoa organizando finanças pessoais','Vida cotidiana','personal'),
 ('Comparar opções de investimento para aposentadoria', 'highrisk','Consultor de investimentos','Finanças e contabilidade','finance'),
 ('Criar campanha de marketing para um novo produto', 'creative','Gerente de marketing','Marketing, mídia e vendas','marketing'),
 ('Escrever roteiro original para um vídeo de divulgação científica', 'creative','Divulgador científico','Marketing, mídia e vendas','marketing'),
 ('Checar se uma notícia viral é verdadeira', 'routine','Jornalista','Marketing, mídia e vendas','marketing'),
 ('Resumir reunião de trabalho em lista de tarefas', 'routine','Assistente administrativo','Gestão e operações','business'),
 ('Preparar currículo direcionado a uma vaga real', 'routine','Pessoa buscando emprego','Vida cotidiana','personal'),
 ('Treinar entrevista de emprego com perguntas e feedback', 'learn','Pessoa buscando emprego','Vida cotidiana','personal'),
 ('Comparar hotéis e organizar roteiro de viagem', 'routine','Pessoa planejando viagem','Vida cotidiana','personal'),
 ('Escolher tratamento para febre de criança usando só IA', 'highrisk','Pai ou mãe','Vida cotidiana','personal'),
 ('Enviar dados pessoais de meus clientes para uma IA pública', 'sensitive','Microempreendedor individual','Vida cotidiana','personal'),
 ('Escrever mensagem pessoal de pedido de desculpas', 'personal','Pessoa cuidando da casa','Vida cotidiana','personal'),

 ('Comparar laudos radiológicos para discutir conduta clínica', 'highrisk','Radiologista','Saúde e assistência','clinical'),
 ('Interpretar um exame de sangue e decidir conduta médica', 'highrisk','Médico de família','Saúde e assistência','clinical'),
 ('Diagnosticar dor torácica usando IA sem revisão médica', 'highrisk','Médico emergencista','Saúde e assistência','clinical'),
 ('Resumir laudos radiológicos para uma discussão acadêmica', 'routine','Radiologista','Saúde e assistência','clinical'),
 ('Preparar aulas de matemática para o ensino médio', 'routine','Professor do ensino médio','Educação','education'),
 ('Preparar um plano de aula de frações', 'routine','Professor do ensino fundamental','Educação','education'),
 ('Revisar normas técnicas de subestações elétricas', 'routine','Engenheiro de energia','Engenharia','engineering'),
 ('Buscar artigos no Google Scholar para revisão sistemática', 'routine','Bibliotecário de pesquisa','Ciência e pesquisa','research'),
 ('Criar revisão sistemática com estratégia PRISMA', 'routine','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Preparar minha defesa de doutorado', 'learn','Doutorando','Ciência e pesquisa','academic'),
 ('Escrever minha monografia ou TCC', 'authorship','Estudante universitário','Vida cotidiana','academic'),
 ('Definir estratégia de análise estatística para meu artigo', 'creative','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Criar script de análise de coorte em Python ou R', 'routine','Epidemiologista','Ciência e pesquisa','research'),
 ('Escrever projeto de pesquisa com inteligência artificial', 'authorship','Mestrando','Ciência e pesquisa','academic'),
 ('Revisar texto e ortografia da dissertação', 'routine','Mestrando','Ciência e pesquisa','academic'),
 ('Organizar referências bibliográficas em formato Vancouver', 'routine','Bibliotecário de pesquisa','Ciência e pesquisa','research'),
 ('Revisar literatura sobre novos biomarcadores clínicos', 'routine','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Criar apresentação de resultados científicos com figuras', 'routine','Pesquisador biomédico','Ciência e pesquisa','research'),
 ('Desenhar experimento de laboratório com hipótese nova', 'creative','Pesquisador biomédico','Ciência e pesquisa','research'),
 ('Analisar dados de ensaios clínicos sem identificadores', 'routine','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Enviar banco de dados de pacientes identificáveis ao ChatGPT', 'sensitive','Pesquisador clínico','Ciência e pesquisa','research'),
 ('Criar relatório financeiro em Excel para minha empresa', 'routine','Analista financeiro','Finanças e contabilidade','finance'),
 ('Resumir um contrato empresarial antes de assinar', 'highrisk','Advogado cível','Direito e regulação','legal'),
 ('Revisar cláusulas de contrato de trabalho', 'highrisk','Advogado trabalhista','Direito e regulação','legal'),
 ('Preparar material para entrevista de emprego', 'routine','Pessoa buscando emprego','Vida cotidiana','personal'),
 ('Escrever e-mail profissional para um cliente', 'routine','Assistente administrativo','Gestão e operações','business'),
 ('Resumir ata de reunião e listar tarefas e responsáveis', 'routine','Gerente de projetos','Gestão e operações','business'),
 ('Preparar apresentação em slides para reunião de trabalho', 'routine','Consultor de gestão','Gestão e operações','business'),
 ('Traduzir um documento técnico para outro idioma', 'routine','Engenheiro de produção','Engenharia','engineering'),
 ('Comparar artigos de revisão sobre tratamento oncológico', 'routine','Oncologista','Saúde e assistência','clinical'),
 ('Criar respostas a mensagens de pacientes no portal médico', 'sensitive','Médico de família','Saúde e assistência','clinical'),
 ('Gerar resumo de prontuário com sistema clínico aprovado', 'highrisk','Enfermeiro assistencial','Saúde e assistência','clinical'),
 ('Criar um plano alimentar individual para paciente com doença renal', 'highrisk','Nutricionista','Saúde e assistência','clinical'),
 ('Analisar desempenho de uma rede neural em dados clínicos', 'routine','Engenheiro biomédico','Engenharia','engineering'),
 ('Revisar projeto de circuito elétrico de alta tensão', 'highrisk','Engenheiro elétrico','Engenharia','engineering'),
 ('Dimensionar estrutura metálica de cobertura comercial', 'highrisk','Engenheiro estrutural','Engenharia','engineering'),
 ('Montar planilha de gestão de estoque de loja', 'routine','Vendedor varejista','Comércio e serviços','hospitality'),
 ('Escrever descrição de produtos para loja online', 'routine','Gestor de comércio eletrônico','Marketing, mídia e vendas','marketing'),
 ('Preparar roteiro original para vídeo do YouTube', 'creative','Criador de conteúdo','Marketing, mídia e vendas','marketing'),
 ('Editar legendas e transcrever uma entrevista', 'routine','Editor de vídeo','Cultura e produção criativa','creativeprof'),
 ('Gerar ilustração para apresentação de engenharia', 'routine','Designer gráfico','Cultura e produção criativa','creativeprof'),
 ('Pesquisar opções de seguro saúde para minha família', 'highrisk','Pessoa organizando finanças pessoais','Vida cotidiana','personal'),
 ('Planejar viagem com crianças e roteiro de passeios', 'routine','Pai ou mãe','Vida cotidiana','personal'),
 ('Criar roteiro de perguntas para uma consulta médica', 'routine','Cuidador familiar','Vida cotidiana','personal'),
 ('Aprender programação para entrevista técnica', 'learn','Pessoa buscando emprego','Vida cotidiana','personal'),
 ('Conferir imposto de renda e deduções declaradas', 'highrisk','Especialista tributário','Finanças e contabilidade','finance'),
 ('Comparar modelos de previsão de demanda de vendas', 'routine','Cientista de dados','Tecnologia e dados','software'),
 ('Depurar falhas de testes automatizados em CI/CD', 'routine','Engenheiro DevOps','Tecnologia e dados','software'),
 ('Criar testes de acessibilidade para um site', 'routine','Desenvolvedor frontend','Tecnologia e dados','software'),
 ('Planejar sprint e priorizar tarefas de desenvolvimento', 'routine','Gerente de produto digital','Tecnologia e dados','software'),
 ('Escrever relatório de incidente de segurança cibernética', 'highrisk','Analista de cibersegurança','Tecnologia e dados','software'),
 ('Avaliar solução de inteligência artificial para diagnóstico médico', 'highrisk','Engenheiro de IA','Tecnologia e dados','software'),

 ('Criar uma planilha para controlar pedidos do meu negócio', 'routine','Microempreendedor individual','Vida cotidiana','personal'),
]

SOURCE_BY_ARCH={
 'research':'research2025', 'clinical':'ama2026', 'engineering':'anthropic2026',
 'software':'anthropic2026', 'education':'gallup2026', 'legal':'thomson2025',
 'finance':'thomson2026', 'business':'openai2026', 'marketing':'mckinsey2025',
 'manufacture':'onet2026', 'construction':'onet2026', 'agro':'onet2026',
 'logistics':'onet2026', 'hospitality':'onet2026', 'creativeprof':'openai2025',
 'social':'onet2026','personal':'openai2025'
}
for p in PROFILES: p['sourceGroup']=SOURCE_BY_ARCH[p['archetype']]

rows=[]
seen=set()
def canon(s):
 s=unicodedata.normalize('NFKD',s.lower())
 return re.sub(r'\s+',' ', ''.join(c for c in s if not unicodedata.combining(c))).strip()
def append(task,category,profession,sector,source,priority='contextual'):
 key=canon(task)
 if key in seen: return False
 seen.add(key)
 rows.append(dict(id=f'u{len(rows)+1:05d}',task=task,category=category,profession=profession,sector=sector,sourceGroup=source,priority=priority))
 return True
for title,cat,role,sect,source in ANCHORS:
 append(title,cat,role,sect,source,'ancora')

# Construção intercalada por profissão, para não esgotar as 10 mil vagas nos
# setores que por acaso aparecem antes no arquivo.
queue=[]
for p in PROFILES:
 candidates=[]
 templates=ARCH[p['archetype']]
 for step in range(len(templates)*len(p['topics'])):
  offset=step % len(templates)
  topic_index=(step // len(templates) + offset) % len(p['topics'])
  subj=p['topics'][topic_index]
  cat,templ=templates[offset]
  candidates.append((templ.format(x=subj),cat,p['profession'],p['sector'],p['sourceGroup']))
 queue.append(candidates)
round_num=0
while len(rows)<10000:
 progress=0
 for i,candidates in enumerate(queue):
  if round_num<len(candidates):
   task,cat,prof,sect,source=candidates[round_num]
   progress+=append(task,cat,prof,sect,source)
   if len(rows)>=10000: break
 if progress==0: break
 round_num+=1
if len(rows)!=10000:
 raise RuntimeError(f'Não gerou 10.000 casos: {len(rows)}, perfis={len(PROFILES)}')

categories=Counter(r['category'] for r in rows)
sectors=Counter(r['sector'] for r in rows)
professions=Counter(r['profession'] for r in rows)
assert len(set(canon(r['task']) for r in rows))==10000
assert len(professions)>=120,(len(professions),professions.most_common(4))
assert len(sectors)>=15,len(sectors)
assert categories['authorship']>100 and categories['routine']>2000

js='/* 10.000 cenários profissionais estruturados. Não são as 10.000 consultas mais frequentes. */\nwindow.ANTES_TASKS='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n'
(ROOT/'catalogo-10000.js').write_text(js,encoding='utf-8')
with (ROOT/'data'/'catalogo-10000.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=['id','task','category','profession','sector','sourceGroup','priority'])
 writer.writeheader();writer.writerows(rows)
(ROOT/'data'/'catalogo-10000.json').write_text(json.dumps(rows,ensure_ascii=False,indent=0),encoding='utf-8')
print('Cenários',len(rows),'Profissões',len(professions),'Setores',len(sectors))
print('Categorias',dict(categories))
print('Setores',dict(sectors))
print('Arquivos JS/CSV/JSON',*[f'{(ROOT/f).stat().st_size/1024:.0f} kB' for f in ('catalogo-10000.js','data/catalogo-10000.csv','data/catalogo-10000.json')])
for kw in ['tese','artigos científicos','prontuários','vigas','programação','orçamento']:
 match=[r['task'] for r in rows if kw.lower() in r['task'].lower()]
 print(kw,match[:4])
