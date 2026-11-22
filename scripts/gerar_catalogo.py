import json,csv,unicodedata,re,collections, pathlib
out=pathlib.Path(__file__).resolve().parents[1]
(out/'data').mkdir(exist_ok=True)

learn_topics='''
matemática básica|frações|porcentagem|álgebra|geometria|trigonometria|cálculo diferencial|cálculo integral|equações diferenciais|álgebra linear|probabilidade|estatística descritiva|inferência estatística|estatística bayesiana|bioestatística|epidemiologia|desenho de estudos clínicos|ensaios clínicos randomizados|análise de sobrevivência|regressão linear|regressão logística|aprendizado de máquina|redes neurais|programação em Python|programação em R|programação em JavaScript|algoritmos|estruturas de dados|bancos de dados SQL|modelagem de dados|visualização de dados|excel avançado|tabelas dinâmicas|análise de dados|método científico|filosofia da ciência|lógica formal|pensamento crítico|leitura crítica de artigos|redação acadêmica|revisão de literatura|formulação de hipóteses|metodologia científica|física clássica|física quântica|termodinâmica|eletromagnetismo|óptica|mecânica dos fluidos|química geral|química orgânica|bioquímica|biologia celular|genética|genômica|biologia molecular|microbiologia|imunologia|anatomia humana|fisiologia humana|neurociência|farmacologia|patologia|oncologia|cardiologia|saúde pública|nutrição|fisiologia do exercício|psicologia cognitiva|psicologia social|psicologia do desenvolvimento|história do Brasil|história mundial|geografia|geopolítica|economia básica|microeconomia|macroeconomia|finanças pessoais|juros compostos|contabilidade|gestão de projetos|gestão de produtos|empreendedorismo|marketing digital|comunicação científica|jornalismo|ética em pesquisa|bioética|direito constitucional|direito civil|direito do trabalho|sociologia|antropologia|filosofia|literatura brasileira|interpretação de textos|gramática portuguesa|ortografia portuguesa|escrita argumentativa|inglês básico|inglês avançado|espanhol|francês|alemão|hebraico|japonês|italiano|chinês mandarim|pronúncia em inglês|compreensão auditiva|oratória|apresentações em público|escrita criativa|desenho à mão|pintura|fotografia|edição de vídeo|composição musical|teoria musical|violão|piano|xadrez|estratégias de negociação|liderança|resolução de conflitos|educação financeira|educação ambiental|mudanças climáticas|sustentabilidade|engenharia biomédica|engenharia elétrica|eletrônica|robótica|segurança da informação|criptografia|arquitetura de computadores|inteligência artificial|história da medicina|vacinas|diagnóstico por imagem|saúde baseada em evidências|testes de hipóteses|técnicas de memorização|planejamento de estudos
'''.strip().split('|')

creative_topics='''
um roteiro de documentário científico|uma série de vídeos educacionais|uma campanha de vacinação|um podcast de ciência|uma newsletter científica|uma experiência interativa para crianças|uma aula de biologia|um experimento de laboratório|uma hipótese sobre câncer|uma hipótese sobre envelhecimento|uma hipótese sobre o microbioma|uma hipótese sobre doenças neurodegenerativas|uma hipótese sobre mudanças climáticas|uma hipótese sobre imunoterapia|uma hipótese sobre sono|uma hipótese sobre memória|uma hipótese sobre aprendizagem|um projeto de pesquisa clínica|um projeto de engenharia biomédica|um projeto social para escolas|um programa de divulgação científica|uma exposição de museu|um aplicativo de educação|um jogo educativo|um jogo de tabuleiro|um projeto de sustentabilidade|uma campanha de reciclagem|uma solução para mobilidade urbana|uma solução para redução de lixo|uma solução para desperdício de alimentos|uma solução para acesso à saúde|uma solução para monitoramento remoto|uma solução para diagnóstico precoce|uma solução para inclusão digital|uma plataforma de aprendizagem|uma ferramenta de pesquisa|um projeto de robótica|um projeto com sensores vestíveis|uma ferramenta para professores|um curso online|uma oficina criativa|um clube de ciências|um evento científico|uma palestra de impacto|um livro de divulgação científica|uma história de ficção científica|um conto|um romance|um roteiro de cinema|uma peça de teatro|uma exposição fotográfica|uma série de ilustrações|um personagem de ficção|uma identidade visual|uma marca educacional|uma campanha publicitária ética|uma estratégia de comunicação|um infográfico|uma animação científica|uma experiência de realidade virtual|um protótipo de produto|um dispositivo de baixo custo|um aplicativo de saúde|uma iniciativa comunitária|uma política pública de educação|uma proposta de pesquisa|uma estratégia para aprender idiomas|um novo método de ensino|uma atividade de sala de aula|um projeto de extensão universitária|uma competição de ciência|uma narrativa sobre descobertas|uma história sobre um cientista|uma abordagem para entrevistas|um formato de vídeo curto|uma série para YouTube|um carrossel educativo|uma apresentação para investidores|uma apresentação de congresso|um pôster científico|uma ação de combate à desinformação|uma campanha sobre saúde mental|uma iniciativa sobre alimentação saudável|uma iniciativa sobre exercício físico|uma forma de explicar genética|uma forma de explicar estatística|uma forma de explicar evolução|uma forma de explicar vacinas|uma forma de explicar inteligência artificial|uma solução de acessibilidade|uma solução para pessoas idosas|uma solução para famílias|uma solução para escolas públicas|uma forma de aproximar cientistas e público|uma campanha de doação de sangue|uma intervenção de saúde pública|uma técnica de storytelling|um projeto de design sustentável|uma iniciativa de cidadania científica|um sistema de triagem de informações|uma ferramenta de checagem de fatos|uma plataforma de colaboração|um projeto de ciência cidadã|um método de visualização de dados|um modelo de negócio para educação|uma estratégia para reduzir vieses
'''.strip().split('|')

routine_topics='''
anotações de reunião|atas de reuniões|e-mails de trabalho|mensagens de atendimento|comentários de clientes|perguntas frequentes|textos de apresentação|legendas de vídeos|transcrições de entrevistas|transcrições de palestras|transcrições de aulas|artigos para newsletter|notas de pesquisa|resumos de conferências|listas de tarefas|planos de projeto|cronogramas de equipe|registros de atividades|relatórios semanais|relatórios mensais|relatórios de vendas|relatórios financeiros|relatórios de desempenho|relatórios de pesquisa|relatórios operacionais|relatórios de suporte|relatórios de qualidade|relatórios de auditoria|propostas comerciais|propostas de patrocínio|propostas de eventos|propostas de cursos|descrições de produtos|descrições de serviços|textos de páginas de vendas|materiais de treinamento|manuais de instrução|guias de uso|documentos de processos|procedimentos operacionais|políticas internas|regras de evento|informações de calendário|agendas de equipe|anotações de leitura|fichamentos de livros|resumos de livros|resumos de artigos públicos|notícias para uma curadoria|referências bibliográficas|citações de artigos|planilhas de orçamento|planilhas de despesas|planilhas de estoque|planilhas de compras|planilhas de projetos|planilhas de acompanhamento|planilhas de contatos públicos|listas de fornecedores|catálogos de produtos|tabelas de preços|listas de inscrições|formulários de avaliação|respostas anônimas de pesquisas|respostas de questionários públicos|resultados de enquetes|dados públicos de trânsito|dados públicos de educação|dados públicos de saúde|dados meteorológicos públicos|dados de pesquisas abertas|tabelas de indicadores|listas de métricas|listas de requisitos|tickets de suporte|registros de bugs|notas de versão|documentação técnica pública|documentação de software|documentação de APIs públicas|exemplos de código|comentários em código|testes de software|erros de compilação|logs públicos de teste|planos de manutenção|inventários de equipamentos|checklists de viagem|roteiros turísticos|itinerários de eventos|programações de conferências|convites profissionais|convites para palestras|documentos de marketing|posts institucionais|mensagens de acompanhamento|textos de FAQ|textos de ajuda|respostas comerciais padrão|anúncios de emprego|descrições de vagas|descrições de atividades|bios profissionais|páginas institucionais|relatórios de mídias sociais|resultados de campanhas|roteiros de apresentação|materiais de onboarding|roteiros de atendimento|planos de comunicação|boletins informativos|artigos de blog|traduções de documentos públicos|correspondências administrativas|resumos de reuniões|relatórios de sustentabilidade|informações de eventos culturais|catálogos de bibliotecas|resumos de seminários|conteúdos de slides|guias de estudo já concluídos|listas de links úteis|fichas de produtos públicos|resumos de entrevistas públicas
'''.strip().split('|')

risk_topics='''
começar um medicamento|interromper um medicamento|alterar a dose de um remédio|interpretar sintomas de uma criança|decidir fazer uma cirurgia|adiar uma consulta médica|substituir uma consulta por chatbot|interpretar um exame de sangue|interpretar uma tomografia|interpretar uma ressonância magnética|interpretar um ECG|investigar uma dor no peito|lidar com uma crise alérgica|avaliar risco de suicídio|avaliar risco de AVC|diagnosticar uma doença|tratar uma infecção|escolher uma vacina|tomar antibiótico|mudar tratamento oncológico|escolher terapia psicológica|avaliar sintomas na gravidez|decidir sobre parto|interromper amamentação|avaliar febre em bebê|escolher uma dieta terapêutica|prescrever suplementos|interpretar um resultado de biópsia|decidir sobre hospitalização|avaliar lesão após queda|comprar uma casa|contratar um financiamento|refinanciar uma dívida|investir toda a poupança|escolher ações individuais|usar alavancagem financeira|resgatar aposentadoria|escolher um seguro|assinar um contrato de alto valor|aceitar proposta de emprego com cláusulas complexas|pedir demissão sem plano financeiro|declarar imposto de renda|abrir empresa com obrigações fiscais|encerrar empresa com dívidas|entrar com ação judicial|responder a uma intimação|assinar acordo judicial|pedir cidadania|pedir visto de imigração|aceitar termos de guarda de uma criança|assinar contrato de aluguel|negociar pensão alimentícia|escolher escola para necessidades especiais|tomar decisão sobre herança|denunciar assédio no trabalho|fazer investimentos de alto risco|avaliar uma ameaça de segurança|ligar um equipamento elétrico perigoso|reparar instalação de gás|alterar sistema de segurança residencial|decidir sobre exposição a produtos químicos|avaliar risco de contaminação|interpretar uma norma técnica de segurança|adotar procedimento clínico invasivo|alterar protocolo de laboratório com material perigoso|tomar uma decisão de emergência|avaliar condição de voo|usar uma ferramenta potencialmente perigosa|escolher tratamento veterinário|avaliar intoxicação de um animal|orientar primeiros socorros|interpretar uma decisão judicial|avaliar uma dívida tributária|escolher tratamento odontológico|avaliar uma crise psiquiátrica|decidir sobre uso de hormônios|orientar doses pediátricas|avaliar risco de incêndio|decidir sobre uma denúncia criminal|avaliar o risco de um investimento imobiliário
'''.strip().split('|')

personal_topics='''
uma carta de amor|uma mensagem de aniversário para minha mãe|uma mensagem de aniversário para meu pai|uma mensagem de aniversário para meu filho|uma mensagem de aniversário para minha filha|uma mensagem de aniversário para minha esposa|uma mensagem de aniversário para meu marido|uma mensagem de aniversário para um amigo|uma mensagem de agradecimento para meus avós|um pedido de desculpas para minha esposa|um pedido de desculpas para meu marido|um pedido de desculpas para minha mãe|um pedido de desculpas para meu pai|um pedido de desculpas para um amigo|uma mensagem de reconciliação|uma declaração de amor|um discurso de casamento|meus votos de casamento|uma carta de despedida|uma homenagem para alguém que morreu|uma mensagem de apoio para um amigo|uma carta para meu filho no futuro|uma carta para minha filha no futuro|uma mensagem de parabéns para um familiar|um agradecimento ao meu orientador|um depoimento pessoal sobre um fracasso|uma carta contando minha história|uma homenagem para uma professora|uma homenagem para um professor|uma mensagem íntima para meu parceiro|uma mensagem íntima para minha parceira|uma mensagem de luto|uma carta sobre minhas crenças|uma mensagem para retomar uma amizade|uma carta de gratidão para minha família|uma homenagem no Dia das Mães|uma homenagem no Dia dos Pais|uma mensagem de perdão|uma conversa importante com meus pais|uma mensagem sobre meus sentimentos
'''.strip().split('|')

sensitive_topics='''
prontuários com dados identificáveis|resultados de exames de pacientes identificáveis|senhas pessoais|tokens de acesso a sistemas|chaves privadas de criptografia|segredos comerciais|código-fonte confidencial da empresa|contratos sigilosos|informações sobre fusões empresariais|listas privadas de clientes|dados bancários de terceiros|dados de cartões de crédito|documentos de identidade de clientes|informações de folha de pagamento|dados pessoais de crianças|informações protegidas por sigilo profissional|gravações privadas de consultas|resultados de pesquisas clínicas confidenciais|anotações médicas identificáveis|dados de recrutamento não autorizados
'''.strip().split('|')

noai_topics='''
uma prova que proíbe o uso de IA|um exame individual sem ferramentas externas|um concurso com regra explícita de não usar IA|um trabalho escolar com proibição de IA|uma avaliação de matemática sem consulta|uma avaliação de redação que exige autoria individual|uma avaliação universitária que proíbe IA|um exercício obrigatório de raciocínio independente|um processo seletivo que proíbe assistentes|uma certificação com uso de IA proibido|um teste de programação sem assistência|um exame de língua estrangeira sem IA|uma entrevista técnica que exige resolução autônoma|uma tarefa de casa com regra de trabalho individual|uma olimpíada científica com regra sem IA|uma olimpíada de matemática com proibição de IA|uma prova prática com regras de autoria|um desafio de lógica sem ajuda externa|um exame de habilitação profissional sem IA|uma avaliação de leitura individual|um concurso de redação que veda IA|uma submissão de texto que exige escrita própria|um teste presencial sem acesso à internet|uma prova com celular proibido|um exame de cálculo sem recursos digitais|uma avaliação de estatística sem uso de IA|uma tarefa de laboratório que proíbe assistência externa|um desafio de criatividade sem recursos de IA|uma competição de programação sem IA|uma prova de história sem ferramentas|uma avaliação de ciências sem IA|um teste de memória com assistência proibida|uma dinâmica seletiva com ajuda externa vedada|um trabalho acadêmico que exige produção independente|um concurso literário com vedação de texto gerado por IA|um desafio de design com proibição de IA|uma avaliação de tradução individual|uma tarefa de resolução autônoma exigida pelo professor|uma simulação de atendimento com regra sem IA
'''.strip().split('|')

spec=[
  ('learn', learn_topics, 140, [
      'Aprender {x} do zero',
      'Estudar {x} para uma prova',
      'Resolver exercícios de {x} sem receber a resposta pronta',
      'Entender os fundamentos de {x} e explicar com minhas palavras',
      'Praticar {x} para desenvolver minha autonomia',
      'Treinar minha memória e compreensão de {x} sem ajuda automática']),
  ('creative',creative_topics,105,[
      'Gerar ideias realmente originais para {x}',
      'Criar um conceito inesperado para {x}',
      'Desenvolver uma abordagem criativa para {x}',
      'Explorar hipóteses e alternativas para {x}',
      'Inventar uma solução diferente para {x}']),
  ('routine',routine_topics,120,[
      'Organizar {x} em categorias claras',
      'Resumir e estruturar {x} para facilitar o trabalho',
      'Padronizar a formatação de {x}',
      'Classificar informações de {x}',
      'Transformar {x} em uma tabela simples',
      'Revisar clareza e consistência de {x}']),
  ('highrisk',risk_topics,80,[
      'Decidir sobre {x} com base apenas na IA',
      'Perguntar à IA se devo fazer {x}',
      'Avaliar riscos de {x} consultando somente um chatbot',
      'Pedir à IA a decisão definitiva sobre {x}',
      'Usar IA para comparar opções relacionadas a {x}']),
  ('personal',personal_topics,40,[
      'Escrever {x} para expressar o que sinto',
      'Pedir a uma IA que escreva {x} por mim',
      'Criar {x} com minhas próprias palavras',
      'Deixar a IA inventar sentimentos em {x}',
      'Usar IA como substituta da minha voz em {x}']),
  ('sensitive',sensitive_topics,20,[
      'Enviar {x} para um chatbot público',
      'Resumir {x} usando IA sem autorização',
      'Classificar {x} numa ferramenta de IA externa',
      'Colar {x} num chat para pedir ajuda',
      'Analisar {x} com IA não aprovada',
      'Compartilhar {x} com um assistente de IA sem garantias adequadas']),
  ('noai',noai_topics,39,[
      'Usar IA durante {x}',
      'Pedir respostas à IA em {x}',
      'Delegar a realização de {x} à IA',
      'Receber respostas automáticas para {x}',
      'Quebrar as regras usando IA em {x}']),
]
all_tasks=[]
for cat,subjects,n,phrases in spec:
  unique=list(dict.fromkeys(s.strip() for s in subjects if s.strip()))
  if len(unique)<n: raise ValueError(f'{cat}: insufficient topics {len(unique)} need {n}')
  for subj in unique[:n]:
    for p in phrases:
      all_tasks.append({'id':f'{cat[:2]}-{len(all_tasks)+1:04d}', 'task':p.format(x=subj), 'category':cat})
assert len(all_tasks)==3000,len(all_tasks)
assert len(set(x['task'] for x in all_tasks))==3000
print('Counts:', collections.Counter(x['category'] for x in all_tasks));print('Chars:',sum(len(x['task']) for x in all_tasks))
js='/* Banco local de 3.000 tarefas. Não envia textos a servidores. */\nwindow.ANTES_TASKS='+json.dumps(all_tasks,ensure_ascii=False,separators=(',',':'))+';\n'
(out/'catalogo-3000.js').write_text(js,encoding='utf-8')
with (out/'data'/'catalogo-3000.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['id','task','category']);w.writeheader();w.writerows(all_tasks)
print('Examples:',all_tasks[0],all_tasks[1800],all_tasks[-1]);print('File bytes', (out/'catalogo-3000.js').stat().st_size)