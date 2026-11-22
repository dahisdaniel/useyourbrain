#!/usr/bin/env python3
"""Gera 50.000 cenários editoriais de IA, com tarefas cotidianas prioritárias.

Não se trata de 50 mil usos observados nem ranking global. A principal diferença
é separar intenções (redigir/responder/arquivar) de meros sinônimos. Cada cenário
ocupacional adiciona contexto concreto; sinônimos ficam em aliases, fora da contagem.
"""
from pathlib import Path
import csv,json,random,re,runpy,unicodedata
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
ROOT.joinpath('catalogo').mkdir(exist_ok=True)
ROOT.joinpath('data').mkdir(exist_ok=True)
BASE=json.loads(ROOT.joinpath('data/catalogo-10000.json').read_text(encoding='utf-8'))
SOURCE=runpy.run_path(str(ROOT/'scripts/gerar_catalogo_10000.py'))
PROFILES=SOURCE['PROFILES']; ARCH=SOURCE['ARCH'];SOURCE_BY_ARCH=SOURCE['SOURCE_BY_ARCH']
ANCHORS=[]
def add(task,category='routine',profession='Pessoas em geral',sector='Vida cotidiana',source='openai2025',intent='general',aliases=None):
    ANCHORS.append((task,category,profession,sector,source,intent,aliases or []))

def block(text,cat='routine',intent='general',role='Pessoas em geral',sect='Vida cotidiana',src='openai2025'):
    for line in text.strip().splitlines():
        line=line.strip()
        if line and not line.startswith('#'):
            task,*aliases=[t.strip() for t in line.split('|')]
            add(task,cat,role,sect,src,intent,aliases)

# Linhas centrais — cada uma é uma tarefa real, e não um sinônimo da linha anterior.
block('''
Escrever um e-mail profissional|redigir email|escrever email|fazer um email|redigir e-mail|compose email|write an email
Responder a um e-mail recebido|responder email|responder e-mail|resposta ao email|reply email|reply to an email|answer an email
Reescrever um e-mail com tom mais educado|deixar email educado|polir email|improve email tone
Resumir um e-mail longo|resumir email|sumarizar email|summarize email
Resumir uma conversa de e-mails|resumir thread de email|resumir troca de emails|summarize email thread
Escrever e-mail cobrando resposta sem soar rude|follow up email|cobrar resposta email
Escrever e-mail de acompanhamento após uma reunião|followup pos reuniao|meeting follow-up email
Escrever e-mail de convite para reunião|convidar para reuniao por email
Escrever e-mail para pedir informações|email solicitando informacoes
Escrever e-mail para solicitar orçamento|solicitar cotacao por email
Escrever e-mail para negociar prazo|negociar deadline por email
Escrever e-mail para pedir reembolso|request refund email
Escrever e-mail de reclamação ao suporte|reclamar com empresa por email
Escrever e-mail de candidatura a uma vaga|email de emprego|job application email
Escrever e-mail ao recrutador|email para rh|email recruiter
Escrever e-mail pedindo uma recomendação profissional|pedir carta de recomendacao por email
Escrever e-mail agradecendo uma entrevista|agradecimento entrevista email
Responder a um cliente por e-mail|reply to client email
Responder a um fornecedor por e-mail|reply vendor email
Responder e-mail com dados de orçamento|responder cotacao por email
Responder e-mail de reclamação do cliente|reply to complaint
Responder um e-mail delicado do chefe|email chefe resposta
Responder convite de reunião por e-mail|reply meeting invitation
Responder e-mail em outro idioma|responder email em ingles
Escrever e-mail formal em inglês|write formal email
Escrever e-mail informal para colegas de trabalho|email informal para colega
Escrever mensagem no Slack para a equipe|slack message
Escrever mensagem no Teams para colegas|teams message
Revisar gramática de e-mail antes de enviar|revisar email|corrigir email
Encurtar um e-mail muito longo|reduzir email
Encontrar um e-mail antigo no Gmail|achar email no gmail|procurar email antigo
Buscar e-mails sobre um assunto no Outlook|search outlook emails
Priorizar minha caixa de entrada|organizar inbox|triagem de email
Identificar e-mails urgentes na caixa de entrada|emails urgentes
Agrupar e-mails por assunto|classificar emails por tema
Criar etiquetas no Gmail para meus e-mails|etiquetas gmail
Criar pastas no Outlook para organizar e-mails|pastas outlook
Arquivar e-mails antigos automaticamente|arquivar email|archive emails
Separar newsletters de mensagens importantes|filtrar newsletter email
Identificar spam e e-mails de phishing|detectar phishing email
Cancelar inscrições de newsletters|unsubscribe emails
Criar filtros automáticos no Gmail|filtros gmail|gmail rules
Criar respostas prontas para e-mails recorrentes|templates de email
Extrair prazos e compromissos de e-mails|extrair tarefas do email
Organizar os anexos recebidos por e-mail|anexos do email
Preparar uma resposta por e-mail com base em documentos|email com anexo e documentos
Criar resumo semanal da minha caixa de entrada|digest semanal de emails
Traduzir um e-mail recebido|translate received email
Identificar tarefas pendentes em uma troca de e-mails|action items email
Escrever uma mensagem de ausência automática|out of office email
''',intent='email',role='Profissional administrativo',sect='Escritório e comunicação',src='openai2025')
block('''
Organizar pastas no computador|organizar pastas|arrumar minhas pastas|organizar diretorios|organize folders
Organizar arquivos no computador|organizar arquivos|arrumar documentos|organize files
Organizar arquivos no Google Drive|organizar google drive|arrumar drive
Organizar arquivos no OneDrive|organizar onedrive
Organizar arquivos no Dropbox|organizar dropbox
Organizar arquivos no iCloud Drive|organizar icloud drive
Organizar a pasta Downloads|limpar downloads|organizar download
Criar estrutura de pastas para projeto de trabalho|hierarquia de pastas
Separar arquivos pessoais e profissionais|separar arquivos
Renomear arquivos em lote|renomear arquivos|batch rename files
Localizar um PDF perdido no computador|achar pdf|procurar arquivo perdido
Buscar documentos por conteúdo em vez do nome|pesquisar dentro dos arquivos
Identificar arquivos duplicados|achar duplicatas arquivo
Identificar documentos desatualizados|documentos velhos
Agrupar PDFs por assunto|organizar pdf
Converter vários arquivos para PDF|convert files to pdf
Extrair tabelas de vários PDFs|extrair tabela pdf
Resumir documentos longos em uma pasta|resumir documentos
Criar índice dos documentos de um projeto|indexar documentos
Padronizar nomes de arquivos de contratos|nomear arquivos
Comparar duas versões de um documento|comparar documento
Identificar alterações entre contratos|diferenças contratos
Classificar recibos em pastas|organizar recibos
Separar notas fiscais por mês|organizar notas fiscais
Organizar documentos do imposto de renda|pasta imposto renda
Organizar documentos para mudança de casa|documentos mudanca
Organizar currículos recebidos para uma vaga|organizar curriculos
Preparar backup de arquivos importantes|backup documentos
Criar checklist para verificar backup|revisar backup
Eliminar arquivos temporários com segurança|limpar arquivos temporarios
Encontrar arquivos grandes que ocupam espaço|localizar arquivos grandes
Organizar materiais de aula em pastas|pastas aulas
Organizar arquivos de um projeto de pesquisa|pastas pesquisa
Organizar fotos e vídeos exportados para o computador|organizar mídia computador
Criar uma planilha de inventário de documentos|inventario documental
''',intent='files',role='Pessoas em geral',sect='Vida cotidiana',src='openai2025')
block('''
Organizar minhas fotos do Google Fotos|organizar fotos google photos|organizar fotos google fotos|arrumar google fotos
Procurar uma foto antiga no Google Fotos|achar foto google fotos|encontrar foto antiga
Encontrar fotos de uma pessoa no Google Fotos|buscar pessoa fotos
Encontrar fotos de uma viagem específica|localizar fotos viagem
Encontrar fotos pelo local em que foram tiradas|fotos pela localizacao
Encontrar fotos pela data|fotos por data
Pesquisar um objeto dentro das minhas fotos|encontrar objeto na foto
Encontrar fotos de documentos e recibos|fotos recibos|fotos documento
Criar álbum de família no Google Fotos|album de familia
Criar álbum de fotos de uma viagem|album viagem
Organizar fotos do bebê por mês|fotos bebe por mes
Montar álbum de aniversário com fotos do celular|album aniversario
Compartilhar álbum de fotos com a família|shared album
Selecionar as melhores fotos para um álbum|escolher melhores fotos
Encontrar fotos duplicadas no Google Fotos|remover fotos duplicadas|duplicated photos
Separar fotos profissionais e pessoais|separar fotos
Organizar capturas de tela do celular|organizar screenshots|organizar prints
Identificar fotos desfocadas para revisão|identificar fotos borradas
Organizar vídeos e fotos do iPhone|organizar fotos iphone
Organizar biblioteca de fotos no iCloud|organizar fotos icloud
Agrupar fotos por evento|organizar fotos por evento
Localizar fotos de um animal de estimação|fotos pet
Encontrar uma foto da placa do carro|buscar placa nas fotos
Encontrar foto de nota fiscal antiga|achar nota fiscal nas fotos
Extrair texto de uma foto de documento|ocr foto
Identificar imagens com dados pessoais antes de compartilhar|privacidade fotos
Escolher fotos para currículo ou perfil profissional|fotos perfil linkedin
Criar legendas para fotos de viagem|legendas fotos viagem
Comparar fotos para escolher a melhor expressão|melhor selfie
Criar uma retrospectiva com fotos do ano|retrospectiva fotos
Gerar lista de fotos que precisam de backup|backup fotos
Organizar fotografias digitalizadas da família|fotos antigas digitalizadas
Buscar fotos usando descrição em linguagem natural|pesquisar fotos usando texto
Separar fotos com rostos de crianças antes de publicar|privacidade criancas fotos
''',intent='photos',role='Pessoas em geral',sect='Vida cotidiana',src='googlephotos')
block('''
Planejar minha agenda da semana|organizar agenda semanal
Encontrar horário livre para reunião|encontrar horario no calendario
Remarcar uma reunião para outro horário|remarcar reuniao
Preparar pauta de reunião|pauta reuniao|agenda meeting
Resumir a transcrição de uma reunião|meeting summary
Criar uma ata de reunião|meeting minutes|ata reuniao
Extrair decisões e responsáveis de uma reunião|action items meeting
Criar lembretes de compromissos|reminders
Reorganizar tarefas atrasadas no calendário|tarefas atrasadas
Planejar blocos de trabalho concentrado|time blocking
Preparar uma lista de tarefas para hoje|to do list
Priorizar minha lista de tarefas|priorizar tarefas
Dividir um projeto grande em tarefas menores|quebrar projeto em tarefas
Organizar tarefas no Trello|trello tasks
Organizar tarefas no Asana|asana tasks
Organizar tarefas no Notion|notion tasks
Consolidar tarefas de e-mails e mensagens|tarefas do email
Criar rotina matinal realista|planejar rotina
Preparar agenda de viagem de negócios|agenda viagem trabalho
Consolidar notas de reuniões da semana|notas reunioes
Escrever um resumo de reunião para enviar por e-mail|email resumo reuniao
Preparar pontos para conversa com meu gestor|one on one manager
Organizar documentos de reunião de diretoria|board meeting documents
Criar cronograma para entrega de projeto|project timeline
Identificar conflitos na minha agenda|calendar conflicts
''',intent='office',role='Profissional administrativo',sect='Escritório e comunicação',src='openai2025')
block('''
Escrever uma apresentação em slides|criar slides|fazer apresentacao powerpoint
Revisar ortografia de um relatório|corrigir relatorio
Resumir um PDF longo|resumir pdf
Traduzir um documento técnico|traduzir pdf
Criar uma tabela em Excel|montar tabela excel
Criar fórmulas para uma planilha|formula excel
Encontrar erros em fórmulas do Excel|debug excel
Criar gráficos a partir de uma planilha|graficos excel
Consolidar várias planilhas do Excel|consolidar planilhas
Limpar dados duplicados em planilha|deduplicar planilha
Analisar uma base de dados no Excel|analise excel
Criar modelo de orçamento no Google Sheets|budget google sheets
Montar relatório mensal de atividades|relatorio mensal
Revisar contrato de prestação de serviços|revisar contrato
Preparar um documento de proposta comercial|proposta comercial
Editar currículo para uma vaga específica|adaptar curriculo vaga
Preparar carta de apresentação para emprego|cover letter
Resumir um artigo de jornal|resumo noticia
Comparar diferentes notícias sobre um acontecimento|comparar noticias
Verificar uma alegação científica antes de compartilhar|fact checking
Pesquisar o histórico de uma empresa|pesquisar empresa
Montar bibliografia para estudo|bibliografia estudo
Preparar perguntas para entrevista de emprego|perguntas entrevista
Avaliar pontos fortes e fracos de opções de carreira|decisao carreira
Planejar compras do supermercado com receitas|lista compras supermercado
Planejar refeições da semana|planejamento refeicoes
Organizar receitas salvas no celular|organizar receitas
Preparar lista de itens para uma viagem|packing list
Montar itinerário de viagem com crianças|roteiro viagem criancas
Comparar hotéis para uma viagem|comparar hoteis
Pesquisar passagens aéreas e regras de bagagem|pesquisar passagem
Pesquisar produtos antes de comprar|comparar produtos
Comparar preços de eletrodomésticos|precos eletrodomesticos
Pesquisar avaliações de escolas e creches|escolas creches
Comparar modelos de cadeirinhas de carro|car seat comparison
Planejar manutenção preventiva da casa|manutencao casa
Fazer lista de compras para obra ou reforma|lista reforma
Organizar contas domésticas do mês|contas mensais
Montar planilha de controle de despesas pessoais|planilha gastos
Identificar assinaturas mensais que não uso|assinaturas desnecessarias
Resumir termos de um contrato de aluguel|contrato aluguel
Planejar uma mudança de apartamento|mudanca apartamento
Pesquisar financiamento imobiliário|pesquisar mortgage
Preparar perguntas para consulta médica|perguntas medico
Entender resultados de um exame sem tomar decisões sozinho|explicar exame
Buscar clínicas e médicos com especialidade específica|encontrar medico
Pesquisar efeitos colaterais de um medicamento|efeitos colaterais medicamento
Entender uma bula de remédio|explicar bula
Organizar dados de treino e corrida|dados treino
Preparar plano para estudar um idioma|estudar ingles
Treinar conversação em inglês|conversacao ingles
Aprender a resolver equações sem a resposta pronta|aprender equacoes
Estudar matemática para prova|estudar matematica
Planejar estudos para concurso público|estudos concurso
Organizar notas e resumos de aula|notas aula
Criar flashcards para revisão|criar flashcards
Praticar perguntas de uma prova oral|simular banca
Pesquisar cursos de especialização|buscar cursos
''',intent='everyday',src='openai2025')
block('''
Escrever uma mensagem sincera de pedido de desculpas|pedir desculpas por mensagem
Escrever uma carta de amor para meu parceiro|carta amor
Escrever mensagem pessoal sobre um assunto delicado|mensagem pessoal delicada
Preparar discurso de casamento com minhas palavras|votos casamento
Escrever um texto de homenagem para alguém da família|homenagem pessoal
''',cat='personal',intent='personal')
block('''
Escrever minha tese de doutorado|redigir tese|escrever a tese|write my dissertation
Escrever minha dissertação de mestrado|redigir dissertacao de mestrado
Escrever capítulo da discussão da minha tese|discussao tese
Escrever interpretação dos resultados do meu artigo científico|interpretar resultados artigo
Escrever resposta aos revisores de um artigo|response to reviewers
Planejar um artigo científico original|estrutura artigo cientifico
Redigir proposta de bolsa de pesquisa|escrever grant proposal
''',cat='authorship',intent='research',role='Pesquisador',sect='Ciência e pesquisa',src='research2025')
block('''
Buscar artigos científicos no PubMed|buscar papers pubmed|buscar estudos pubmed|literature search
Buscar artigos no Google Scholar|google scholar search
Buscar artigos na Scopus|pesquisar na scopus
Montar estratégia de busca booleana de literatura|boolean search
Identificar artigos científicos recentes sobre um tema|latest papers
Identificar revisões sistemáticas relevantes|achar systematic review
Comparar resultados de dois ensaios clínicos|comparar trials
Montar tabela de evidências para revisão sistemática|evidence table
Identificar DOI de referências citadas|verificar doi
Verificar se uma referência científica existe|validar citacao
Extrair critérios de inclusão de um ensaio clínico|inclusion criteria
Organizar PDFs de artigos científicos em Zotero|organizar zotero
Criar biblioteca de referências no Mendeley|organizar mendeley
Resumir artigo científico apontando limitações|resumir paper
Encontrar lacunas na literatura científica|gaps in literature
Preparar protocolo de revisão sistemática|systematic review protocol
Construir fluxograma PRISMA de triagem de artigos|prisma flow
Preparar código para análise de dados de pesquisa|analysis code
Conferir pressupostos de modelo estatístico|model assumptions
Explorar dados experimentais e criar gráficos|dados experimento
Checar erros em script Python de análise científica|debug research python
''',intent='research',role='Pesquisador',sect='Ciência e pesquisa',src='research2025')
block('''
Formular hipótese científica original|criar hipotese pesquisa
Desenhar experimento que diferencie hipóteses concorrentes|planejar experimento
Propor mecanismo alternativo para um resultado experimental|interpretacao alternativa
Criar ideia original para projeto de pesquisa|ideia projeto pesquisa
''',cat='creative',intent='research',role='Pesquisador',sect='Ciência e pesquisa',src='research2025')
block('''
Buscar diretrizes médicas atualizadas|buscar guidelines medicos
Resumir revisões sistemáticas para discussão clínica|resumir literatura medica
Criar material educativo para pacientes|patient education
Preparar apresentação para reunião médica|case conference
Preparar perguntas para discussão de caso clínico|case discussion
Criar rascunho de carta de encaminhamento sem dados identificáveis|referral letter draft
Montar checklist de alta hospitalar|hospital discharge checklist
Organizar estudos de atualização médica|continuing medical education
''',intent='clinical',role='Médico',sect='Saúde e assistência',src='ama2026')
block('''
Definir diagnóstico de paciente baseado apenas em resposta de IA|diagnosticar paciente com chatgpt
Escolher dose de medicamento sem revisão clínica|dosagem remedio com ia
Decidir se um paciente precisa de cirurgia usando somente IA|decisao cirurgica com ia
Interpretar tomografia e definir conduta sem revisão médica|laudo tc sozinho
Interpretar um ECG para atendimento de emergência sem supervisão|interpretar ecg ia
Determinar tratamento oncológico apenas com chatbot|tratamento cancer ia
Tomar decisão de investimento com base apenas em chatbot|decidir investir com chatgpt
Aprovar estrutura de ponte sem revisão de engenharia|aprovar projeto ponte ia
Liberar software de dispositivo médico sem validação|software clinico sem validacao
''',cat='highrisk',intent='clinical',role='Profissional especializado',sect='Saúde e assistência',src='ama2026')
block('''
Enviar prontuário identificável de paciente a chatbot público|upload prontuario em ia
Colar dados bancários privados de clientes em IA não aprovada|dados privados banco chatbot
Enviar contrato confidencial de cliente para chatbot público|contrato sigiloso chatgpt
Enviar foto de documento de identidade a ferramenta desconhecida|foto identidade chatbot
Colar senhas ou chaves de API em chatbot público|colocar senha na ia
Subir dados de participantes de pesquisa não anonimizados|dados sujeitos pesquisa
Enviar fotos privadas de crianças a serviço sem consentimento|fotos criancas ia
''',cat='sensitive',intent='privacy',role='Profissional',sect='Privacidade e segurança',src='nist')
block('''
Depurar código Python com erro|debug python
Criar testes automatizados para API|api testing
Explicar uma mensagem de erro no JavaScript|javascript error
Criar uma query SQL complexa|sql query
Revisar performance de uma consulta SQL|sql optimization
Gerar documentação de uma API REST|api docs
Revisar código em pull request|code review
Criar testes end-to-end com Playwright|e2e tests
Refatorar uma função grande em componentes menores|refactor function
Criar um script para organizar arquivos em lote|file automation script
Criar aplicativo web responsivo|responsive site
Corrigir um bug em CSS para celular|css mobile bug
Montar pipeline de CI/CD no GitHub Actions|github actions
Revisar logs para identificar causa de erro|logs debugging
Migrar banco de dados PostgreSQL|database migration
''',intent='coding',role='Desenvolvedor de software',sect='Tecnologia e dados',src='anthropic2026')
block('''
Revisar especificações de um circuito elétrico|electrical circuit review
Calcular queda de tensão de um cabo|voltage drop
Conferir unidades de um cálculo de engenharia|engineering units
Resumir relatório de ensaio de materiais|material test report
Criar checklist de inspeção de equipamento|inspection checklist
Montar matriz de requisitos técnicos|requirements matrix
Pesquisar normas técnicas aplicáveis a projeto|technical standards search
Comparar fichas técnicas de sensores|sensor datasheets
Analisar tendência de falha em dados de manutenção|predictive maintenance
Preparar relatório de não conformidade de fábrica|nonconformance report
''',intent='engineering',role='Engenheiro',sect='Engenharia',src='anthropic2026')
block('''
Preparar apresentação de resultados para diretoria|board presentation
Resumir indicadores financeiros do trimestre|quarterly kpis
Criar briefing executivo para decisão estratégica|executive briefing
Preparar pauta para reunião de conselho|board agenda
Montar análise SWOT de unidade de negócio|swot analysis
Comparar concorrentes no mercado|competitor research
Preparar perguntas para reunião com investidores|investor questions
Organizar feedbacks de clientes por prioridade|customer feedback
Transformar pesquisa de mercado em plano de ação|market action plan
Preparar relatório de desempenho de equipe|team performance report
Organizar follow-ups de reuniões de liderança|leadership followups
''',intent='executive',role='Executivo',sect='Gestão e operações',src='openai2026')
block('''
Escrever campanha de marketing para lançamento de produto|marketing campaign
Criar calendário de conteúdo para Instagram|instagram content calendar
Resumir comentários de clientes em redes sociais|social listening
Preparar roteiro original para vídeo de divulgação científica|science video script
Revisar legenda de Reel em português|reel caption
Preparar descrição de produto para loja online|product descriptions
Organizar pedidos de clientes em planilha|orders spreadsheet
Criar resposta a comentário crítico de cliente|customer complaint response
Criar chatbot de atendimento baseado em FAQ|customer support chatbot
Preparar anúncio de vaga de emprego|job description
Triar currículos com critérios transparentes|resume screening
Organizar planejamento de turnos da equipe|staff shifts
''',intent='business',role='Profissional de negócios',sect='Gestão e operações',src='openai2026')

# Transformações contextuais: atividades materialmente distintas que as pessoas fazem
# sobre artefatos e assuntos específicos. Sinônimos NÃO geram linhas próprias.
EMAIL_CONTEXTS=[
 ('projeto de trabalho','um gestor'),('reunião com cliente','o cliente'),('atraso na entrega','um fornecedor'),
 ('proposta comercial','um prospect'),('aprovação de orçamento','a diretoria'),('vaga de emprego','o recrutador'),
 ('atividade da escola','a coordenação'),('consulta médica','a clínica'),('prazo de pagamento','o financeiro'),
 ('dúvida sobre serviço','o suporte'),('reembolso de compra','a loja'),('convite de evento','a organização'),
 ('cobrança de fatura','o cliente'),('material da pesquisa','o coautor'),('encontro de networking','um contato'),
 ('alteração de contrato','o jurídico'),('atualização do cronograma','a equipe'),('pedido de orçamento','um prestador'),
 ('documentação de seguro','a seguradora'),('reunião de condomínio','o síndico'),
]
for context,who in EMAIL_CONTEXTS:
    for verb,cat in [('Escrever','routine'),('Responder','routine'),('Resumir os e-mails sobre','routine'),('Preparar follow-up sobre','routine')]:
        task = f'{verb} um e-mail para {who} sobre {context}' if verb in ('Escrever','Responder') else f'{verb} {context}'
        add(task,cat,'Profissional administrativo','Escritório e comunicação','openai2025','email')

FILE_CONTEXTS=['documentos de clientes','documentos da empresa','PDFs de artigos científicos','faturas e recibos','contratos assinados','arquivos da escola','documentos financeiros','manuais de equipamentos','resultados de laboratório','notas de reunião','fotos de viagens','vídeos do celular','comprovantes de pagamento','documentos do condomínio','material de onboarding','relatórios de projeto','arquivos de design','dados de experimentos','planilhas mensais','documentos pessoais','arquivos do Google Drive','arquivos do OneDrive','pasta Downloads','arquivos recebidos no WhatsApp']
for obj in FILE_CONTEXTS:
    for t in ['Organizar {x} por assunto','Localizar {x} rapidamente','Identificar versões antigas de {x}','Criar estrutura de pastas para {x}','Classificar {x} por data','Preparar inventário de {x}','Comparar versões de {x}']:
        add(t.format(x=obj),'routine','Pessoas em geral','Vida cotidiana','openai2025','files')

PHOTO_CONTEXTS=['fotos do Google Fotos','fotos do iCloud','fotos de viagens','fotos da família','fotos do celular','fotos do bebê','fotos de animais de estimação','fotos de eventos profissionais','fotos de produtos','fotos da reforma','fotos digitalizadas antigas','fotos de documentos','capturas de tela']
for obj in PHOTO_CONTEXTS:
    for t in ['Organizar {x} por data','Buscar {x} com descrição em linguagem natural','Criar álbum temático de {x}','Separar duplicatas de {x} para revisão','Selecionar as melhores {x} para compartilhar','Localizar {x} pelo local','Preparar backup de {x}']:
        add(t.format(x=obj),'routine','Pessoas em geral','Vida cotidiana','googlephotos','photos')

# Os 10.000 casos anteriores preservam a amplitude já existente; as novas
# entradas surgem de tarefas adicionais em contextos ocupacionais reais.
seen=set();rows=[]
def norm(s):
 s=unicodedata.normalize('NFKD',s.casefold())
 return re.sub(r'\s+',' ',''.join(c for c in s if not unicodedata.combining(c))).strip()
def push(task,category,profession,sector,source,intent,aliases,priority):
 task=task.strip(); key=norm(task)
 if key in seen:return False
 seen.add(key)
 rows.append({'id':f'c{len(rows)+1:05d}','task':task,'category':category,'profession':profession,'sector':sector,'sourceGroup':source,'intent':intent,'priority':priority,'aliases':aliases})
 return True
for t,c,p,s,src,intent,alias in ANCHORS:push(t,c,p,s,src,intent,alias,'essencial')
for r in BASE:
 intent = ('email' if re.search(r'\be.?mail\b',norm(r['task'])) else
 'photos' if re.search(r'foto|photo|imagem',norm(r['task'])) else
 'files' if re.search(r'pasta|arquivo|diretorio',norm(r['task'])) else
 'research' if r['sector']=='Ciência e pesquisa' else
 'clinical' if r['sector']=='Saúde e assistência' else
 'engineering' if r['sector']=='Engenharia' else
 'coding' if r['sector']=='Tecnologia e dados' else
 'office' if r['sector'] in ('Gestão e operações','Educação') else 'general')
 push(r['task'],r['category'],r['profession'],r['sector'],r['sourceGroup'],intent,[],'setorial')

# Templates especializados: contextos distintos do trabalho, não paráfrases da
# mesma pergunta. Uma variação contém tema ou artefato específico de cada ocupação.
TEMPLATES={
'research':[
('routine','Montar uma estratégia de busca reprodutível para {x}'),('routine','Importar referências sobre {x} no Zotero e verificar DOI'),('routine','Extrair as características de coorte dos artigos sobre {x}'),('routine','Construir tabela de risco de viés para estudos de {x}'),('routine','Comparar os endpoints dos ensaios publicados sobre {x}'),('routine','Documentar scripts de análise estatística relacionados a {x}'),('routine','Criar gráficos de sensibilidade de modelos para {x}'),('routine','Preparar slides do seminário de laboratório sobre {x}'),('routine','Identificar referências citadas incorretamente sobre {x}'),('routine','Comparar variáveis de um dicionário de dados de {x}'),('routine','Conferir se parâmetros de modelo de {x} estão bem descritos'),('routine','Organizar documentação de protocolo pré-registrado de {x}'),('routine','Revisar consistência entre tabelas e texto em estudo de {x}'),('routine','Preparar checklist CONSORT ou STROBE para pesquisa de {x}'),('routine','Simular tamanho amostral para estudo de {x} e revisar premissas'),('routine','Criar tabelas descritivas reproduzíveis de {x}'),('routine','Buscar bases públicas adequadas à investigação de {x}'),('routine','Revisar código em R para análise de {x}'),('routine','Revisar código em Python para análise de {x}'),('routine','Avaliar gráficos alternativos para mostrar resultados de {x}'),('creative','Propor hipótese rival à explicação prevalente de {x}'),('creative','Criar controles negativos e positivos para experimento de {x}'),('creative','Planejar análise exploratória para achado inesperado em {x}'),('authorship','Redigir seção de discussão autoral sobre {x}'),('authorship','Defender oralmente a contribuição original do meu estudo de {x}'),('learn','Treinar interpretação de intervalos de confiança em estudo de {x}'),('highrisk','Avaliar implicações éticas da coleta de dados de {x}'),('sensitive','Compartilhar dados identificáveis de participantes de {x} em ferramenta pública'),
],
'clinical':[
('routine','Localizar diretrizes clínicas originais sobre {x}'),('routine','Comparar achados de metanálises recentes sobre {x}'),('routine','Preparar ficha educativa para pacientes sobre {x}'),('routine','Criar checklist administrativo para atendimento de {x}'),('routine','Padronizar vocabulário de documentação clínica sobre {x}'),('routine','Preparar material de treinamento da equipe sobre {x}'),('routine','Revisar cronologia de recomendações de guidelines de {x}'),('routine','Localizar informações de bula e interações para {x}'),('routine','Organizar perguntas para discussão multidisciplinar de {x}'),('routine','Resumir diferenças entre escalas clínicas usadas em {x}'),('routine','Preparar fluxograma de encaminhamento de {x} para revisão médica'),('routine','Transformar explicação técnica de {x} em linguagem acessível'),('routine','Gerar lista de artigos para reunião clínica de {x}'),('routine','Revisar consistência de dados agregados de qualidade em {x}'),('routine','Preparar proposta de auditoria de qualidade sobre {x}'),('routine','Comparar formulários de consentimento informados sobre {x}'),('learn','Treinar raciocínio diagnóstico em caso simulado de {x}'),('learn','Estudar critérios de avaliação para certificação sobre {x}'),('creative','Propor pergunta de pesquisa translacional sobre {x}'),('highrisk','Escolher conduta para paciente com {x} usando apenas uma resposta do chatbot'),('highrisk','Liberar laudo de exame relacionado a {x} sem revisão competente'),('highrisk','Definir dose ou suspensão de medicamento para {x} sem validação'),('highrisk','Aplicar escore preditivo de {x} sem validação local'),('highrisk','Automatizar priorização de pacientes com {x} sem supervisão'),('sensitive','Enviar áudio identificável de consulta sobre {x} a chatbot público'),('sensitive','Enviar dados privados de paciente com {x} a serviço não aprovado'),
],
'engineering':[
('routine','Localizar versão vigente da norma técnica de {x}'),('routine','Comparar fichas técnicas de componentes para {x}'),('routine','Revisar unidades e premissas em cálculo de {x}'),('routine','Criar planilha de ensaios de validação de {x}'),('routine','Construir matriz de requisitos para {x}'),('routine','Escrever documentação de procedimento de ensaio de {x}'),('routine','Criar checklist de inspeção preliminar de {x}'),('routine','Resumir manual de manutenção referente a {x}'),('routine','Analisar dados agregados de falha de {x}'),('routine','Comparar orçamento de fornecedores para {x}'),('routine','Preparar relatório de causa-raiz de falha de {x}'),('routine','Gerar script para verificar consistência de dados de {x}'),('routine','Criar apresentação técnica para revisão de projeto de {x}'),('routine','Comparar cronogramas de execução de {x}'),('routine','Preparar plano de testes de regressão para {x}'),('routine','Organizar rastreabilidade de materiais usados em {x}'),('routine','Documentar mudanças de especificação em {x}'),('routine','Montar tabela de calibração de instrumentos para {x}'),('creative','Explorar projeto alternativo que reduza custo de {x}'),('creative','Propor mecanismos de falha não considerados para {x}'),('learn','Aprender a calcular margens de segurança de {x}'),('highrisk','Aprovar projeto de segurança de {x} sem verificação de engenheiro habilitado'),('highrisk','Liberar equipamento de {x} sem ensaio de validação'),('sensitive','Enviar arquivos CAD confidenciais de {x} a chatbot público'),
],
'software':[
('routine','Criar testes unitários para {x}'),('routine','Gerar script de migração para {x}'),('routine','Depurar erro intermitente envolvendo {x}'),('routine','Revisar dependências de segurança usadas em {x}'),('routine','Escrever documentação técnica de {x}'),('routine','Revisar desempenho e gargalos de {x}'),('routine','Explicar stack trace de erro em {x}'),('routine','Criar mock de dados de teste para {x}'),('routine','Montar testes end-to-end de {x}'),('routine','Preparar consulta SQL de auditoria para {x}'),('routine','Construir dashboard de observabilidade de {x}'),('routine','Revisar tratamento de exceções de {x}'),('routine','Criar guia de troubleshooting de {x}'),('routine','Propor estrutura de pull request de {x}'),('routine','Comparar padrões arquiteturais adequados a {x}'),('routine','Desenhar estratégia de rollback de {x}'),('routine','Revisar documentação de API usada por {x}'),('routine','Criar casos de teste para entradas inválidas em {x}'),('routine','Criar matriz de compatibilidade de {x}'),('routine','Gerar plano de refatoração incremental de {x}'),('creative','Explorar alternativas de arquitetura para {x}'),('learn','Aprender a implementar {x} sem receber código pronto'),('highrisk','Implantar alteração crítica de {x} diretamente sem revisão e testes'),('sensitive','Colar tokens de produção de {x} em chatbot público'),
],
'education':[
('routine','Criar plano de aula sobre {x}'),('routine','Preparar rubrica de avaliação para atividade de {x}'),('routine','Gerar exercícios de revisão sobre {x}'),('routine','Organizar materiais didáticos sobre {x}'),('routine','Criar slides para explicar {x}'),('routine','Preparar quiz de verificação de compreensão de {x}'),('routine','Adaptar explicação de {x} para diferentes níveis'),('routine','Planejar sequência de aulas sobre {x}'),('routine','Revisar erros conceituais em material sobre {x}'),('routine','Construir lista de fontes confiáveis sobre {x}'),('routine','Preparar atividades práticas de {x}'),('routine','Analisar resultados agregados de exercícios de {x}'),('routine','Montar calendário de avaliações de {x}'),('routine','Preparar resumo de reunião pedagógica sobre {x}'),('creative','Criar experiência didática original para ensinar {x}'),('learn','Aprender a resolver {x} por conta própria'),('learn','Praticar prova sobre {x} sem consultar a solução'),('highrisk','Atribuir notas finais para alunos de {x} apenas pela IA'),('sensitive','Enviar informações identificáveis de alunos de {x} a chatbot público'),
],
'legal':[
('routine','Localizar jurisprudência atual sobre {x} e conferir acórdãos'),('routine','Organizar documentos de processo relacionado a {x}'),('routine','Criar checklist de cláusulas aplicáveis a {x}'),('routine','Construir linha do tempo dos fatos em caso de {x}'),('routine','Comparar redações de cláusulas de {x}'),('routine','Preparar primeiro rascunho de comunicação sobre {x}'),('routine','Resumir mudanças legislativas relevantes a {x}'),('routine','Revisar inconsistências formais de documento de {x}'),('routine','Preparar lista de documentos necessários para {x}'),('routine','Criar tabela de prazos e marcos de processo de {x}'),('routine','Organizar provas e fontes documentais de {x}'),('routine','Montar questionário de entrevista inicial sobre {x}'),('routine','Preparar slides de treinamento de equipe sobre {x}'),('creative','Explorar argumentos alternativos em hipótese de {x}'),('highrisk','Assinar parecer jurídico definitivo de {x} sem revisão humana'),('highrisk','Definir estratégia processual de {x} só pelo chatbot'),('sensitive','Enviar documentos sigilosos de caso de {x} a IA pública'),
],
'finance':[
('routine','Categorizar despesas agregadas sobre {x}'),('routine','Criar roteiro de conciliação de contas de {x}'),('routine','Conferir fórmulas de demonstrativo relacionado a {x}'),('routine','Preparar tabela de cenários financeiros de {x}'),('routine','Resumir notas explicativas referentes a {x}'),('routine','Organizar faturas e recibos associados a {x}'),('routine','Criar dashboard gerencial de indicadores de {x}'),('routine','Montar checklist de auditoria preliminar para {x}'),('routine','Revisar consistência de premissas em orçamento de {x}'),('routine','Construir cronograma de fechamento relacionado a {x}'),('routine','Identificar divergências entre planilhas de {x}'),('routine','Preparar perguntas para consultor sobre {x}'),('routine','Conferir nomenclatura e formatação de relatórios de {x}'),('routine','Pesquisar documentação regulatória sobre {x}'),('creative','Propor indicadores alternativos para acompanhar {x}'),('highrisk','Autorizar operação financeira de {x} só pela IA'),('sensitive','Compartilhar informações bancárias identificáveis de {x} com serviço não autorizado'),
],
'business':[
('routine','Redigir e-mail de acompanhamento sobre {x}'),('routine','Preparar pauta de reunião de resultados de {x}'),('routine','Resumir indicadores de desempenho referentes a {x}'),('routine','Montar checklist de entrega de {x}'),('routine','Criar briefing para diretoria sobre {x}'),('routine','Organizar responsabilidades e prazos de {x}'),('routine','Comparar propostas comerciais relacionadas a {x}'),('routine','Preparar comunicação interna sobre {x}'),('routine','Consolidar feedbacks da equipe sobre {x}'),('routine','Preparar slides de decisão de {x}'),('routine','Revisar relatórios semanais de {x}'),('routine','Criar FAQ interno sobre {x}'),('routine','Montar roteiro de entrevista com clientes de {x}'),('routine','Analisar comentários de pesquisa de satisfação de {x}'),('routine','Gerar relatório de pendências de {x}'),('routine','Criar análise de custos preliminar para {x}'),('routine','Preparar roteiro de negociação de {x}'),('routine','Organizar histórico de mensagens sobre {x}'),('creative','Explorar alternativas de estratégia para {x}'),('highrisk','Tomar decisão de alto impacto em {x} só por recomendação da IA'),('sensitive','Enviar dados confidenciais de negociação sobre {x} a chatbot público'),
],
'marketing':[
('routine','Escrever e-mail de campanha sobre {x}'),('routine','Criar plano de calendário de conteúdo sobre {x}'),('routine','Preparar relatório de métricas de campanha de {x}'),('routine','Resumir comentários de clientes sobre {x}'),('routine','Criar variações de anúncio para {x}'),('routine','Revisar copy de landing page de {x}'),('routine','Comparar canais de aquisição de público para {x}'),('routine','Pesquisar termos relevantes de SEO para {x}'),('routine','Preparar roteiro de entrevista de público de {x}'),('routine','Organizar ativos de design de campanha de {x}'),('routine','Criar briefing de fotógrafo sobre {x}'),('routine','Conferir consistência de identidade de marca em {x}'),('routine','Planejar sequência de mensagens de pós-venda para {x}'),('routine','Analisar dúvidas mais frequentes de clientes sobre {x}'),('creative','Criar conceito de campanha original para {x}'),('highrisk','Publicar alegação de saúde sobre {x} sem validar evidências'),('sensitive','Enviar lista privada de clientes de {x} a chatbot público'),
],
'manufacture':[
('routine','Criar checklist de inspeção de lote de {x}'),('routine','Documentar procedimento de {x}'),('routine','Analisar tempos de parada associados a {x}'),('routine','Organizar relatório de produtividade de {x}'),('routine','Comparar parâmetros de processo de {x}'),('routine','Criar plano de manutenção de equipamento de {x}'),('routine','Gerar lista de peças de reposição de {x}'),('routine','Preparar planilha de perdas de {x}'),('routine','Organizar fichas de conformidade de {x}'),('routine','Resumir ocorrências de turno de {x}'),('routine','Montar plano de treinamento operacional de {x}'),('routine','Conferir divergências entre medições de {x}'),('creative','Explorar melhoria de processo em {x}'),('highrisk','Liberar lote com falha crítica de {x} com base apenas na IA'),('sensitive','Enviar segredo industrial de {x} para chatbot público'),
],
'construction':[
('routine','Criar cronograma de obra relacionado a {x}'),('routine','Revisar documentação de medição de {x}'),('routine','Organizar diário de obra de {x}'),('routine','Criar checklist de vistoria de {x}'),('routine','Conferir quantitativos de materiais de {x}'),('routine','Preparar planilha de custos de {x}'),('routine','Comparar orçamentos de empreiteiros de {x}'),('routine','Organizar solicitações de informação de {x}'),('routine','Criar matriz de pendências de obra de {x}'),('routine','Resumir reunião de obra referente a {x}'),('routine','Preparar apresentação do andamento de {x}'),('creative','Explorar alternativas de implantação de {x}'),('highrisk','Aprovar segurança estrutural de {x} somente pela IA'),('sensitive','Enviar plantas confidenciais de {x} para IA pública'),
],
'agro':[
('routine','Organizar dados de campo referentes a {x}'),('routine','Preparar tabela de rendimento de {x}'),('routine','Comparar normas ambientais relacionadas a {x}'),('routine','Resumir estudos técnicos sobre {x}'),('routine','Criar calendário operacional de {x}'),('routine','Conferir consistência de medições de {x}'),('routine','Documentar vistoria técnica de {x}'),('routine','Montar matriz de risco preliminar de {x}'),('routine','Criar relatório para órgão regulador sobre {x}'),('routine','Preparar checklist de monitoramento de {x}'),('routine','Comparar fornecedores de equipamentos para {x}'),('creative','Explorar métodos alternativos de manejo de {x}'),('highrisk','Decidir aplicação de produto tóxico em {x} só pela IA'),('sensitive','Enviar dados sigilosos de propriedade associados a {x} a chatbot público'),
],
'logistics':[
('routine','Criar planilha de roteirização de {x}'),('routine','Analisar atrasos recorrentes em {x}'),('routine','Preparar comunicado sobre ocorrência em {x}'),('routine','Organizar comprovantes de entrega de {x}'),('routine','Comparar transportadoras para {x}'),('routine','Criar indicadores de performance de {x}'),('routine','Revisar divergências de estoque de {x}'),('routine','Consolidar relatórios de entregas de {x}'),('routine','Criar checklist de conferência de {x}'),('routine','Preparar plano de contingência de {x}'),('routine','Gerar relatório de custo por rota de {x}'),('creative','Explorar alternativas para reduzir atrasos em {x}'),('highrisk','Autorizar transporte perigoso de {x} sem validação de segurança'),('sensitive','Compartilhar dados identificáveis de clientes de {x} com chatbot público'),
],
'hospitality':[
('routine','Responder e-mail de cliente sobre {x}'),('routine','Criar FAQ de dúvidas de clientes sobre {x}'),('routine','Montar escala de atendimento de {x}'),('routine','Preparar descrição de serviços de {x}'),('routine','Resumir reclamações recorrentes sobre {x}'),('routine','Preparar lista de fornecedores de {x}'),('routine','Organizar reservas e horários de {x}'),('routine','Criar checklist de abertura relacionado a {x}'),('routine','Comparar orçamentos de suprimentos de {x}'),('routine','Escrever instruções para equipe sobre {x}'),('routine','Preparar relatório de vendas de {x}'),('routine','Revisar fichas de produtos de {x}'),('creative','Desenvolver proposta de experiência original para {x}'),('highrisk','Ignorar exigências sanitárias ou de segurança de {x} seguindo apenas IA'),('sensitive','Enviar nomes e telefones de clientes de {x} a serviço sem autorização'),
],
'creativeprof':[
('routine','Revisar legenda de publicação sobre {x}'),('routine','Transcrever entrevista relacionada a {x}'),('routine','Criar cronograma de edição de conteúdo sobre {x}'),('routine','Organizar arquivos visuais de projeto de {x}'),('routine','Gerar versões curtas de conteúdo sobre {x}'),('routine','Verificar fontes e fatos de conteúdo sobre {x}'),('routine','Preparar roteiro técnico de produção de {x}'),('routine','Criar checklist de direitos autorais de {x}'),('routine','Resumir comentários do público de {x}'),('routine','Revisar acessibilidade e legendagem de {x}'),('routine','Montar pauta de entrevista sobre {x}'),('creative','Criar conceito narrativo original para {x}'),('creative','Explorar caminhos estéticos diferentes para {x}'),('highrisk','Publicar informação de alto risco sobre {x} sem checagem'),('sensitive','Enviar material audiovisual privado de {x} a serviço não autorizado'),
],
'social':[
('routine','Criar formulário de atendimento para {x}'),('routine','Organizar relatórios de impacto de {x}'),('routine','Preparar comunicação acessível sobre {x}'),('routine','Revisar materiais de orientação de {x}'),('routine','Consolidar indicadores agregados sobre {x}'),('routine','Criar checklist de encaminhamento de {x}'),('routine','Resumir políticas públicas relacionadas a {x}'),('routine','Preparar relatório para financiadores de {x}'),('routine','Montar calendário de atividades de {x}'),('routine','Organizar perguntas frequentes de atendimento sobre {x}'),('creative','Propor ações alternativas para melhorar {x}'),('highrisk','Tomar decisão sobre proteção de vulneráveis em {x} só pela IA'),('sensitive','Enviar dados identificáveis de famílias atendidas em {x} à IA pública'),
],
'personal':[
('routine','Planejar calendário de tarefas pessoais sobre {x}'),('routine','Comparar informações de diferentes sites sobre {x}'),('routine','Criar checklist para organizar {x}'),('routine','Montar tabela de alternativas para {x}'),('routine','Pesquisar orientações públicas oficiais sobre {x}'),('routine','Resumir artigos sobre {x} com fontes'),('routine','Organizar documentos pessoais sobre {x}'),('routine','Criar lista de perguntas relevantes sobre {x}'),('routine','Preparar lista de compras para {x}'),('routine','Comparar preços e condições para {x}'),('routine','Criar lembrete recorrente de {x}'),('routine','Localizar e classificar arquivos sobre {x}'),('creative','Explorar ideias de lazer relacionadas a {x}'),('learn','Aprender fundamentos de {x} sem resposta pronta'),('highrisk','Tomar decisão de saúde ou segurança sobre {x} só pela IA'),('sensitive','Enviar dados privados da família sobre {x} a aplicativo não autorizado'),
]
}
assert set(TEMPLATES)==set(ARCH),(set(ARCH)-set(TEMPLATES))

# Anotar intenção de cada template para escolher estudos pertinentes.
def infer_intent(task,arch):
 k=norm(task)
 if 'e-mail' in k or 'email' in k:return 'email'
 if 'foto' in k or 'photos' in k:return 'photos'
 if re.search(r'\b(pasta|arquivo|pdfs?|documento|drive|onedrive|dropbox)\b',k):
  return 'files' if arch=='personal' else 'office'
 return {'research':'research','clinical':'clinical','engineering':'engineering','software':'coding','education':'education','legal':'legal','finance':'finance','business':'executive','marketing':'business','manufacture':'engineering','construction':'engineering','agro':'engineering','logistics':'office','hospitality':'business','creativeprof':'creative','social':'office','personal':'everyday'}.get(arch,'general')

# Intercalar perfis e templates para representar profissões com equilíbrio.
queue=[]
for p in PROFILES:
 arch=p['archetype'];todos=ARCH[arch]+TEMPLATES[arch]
 seq=[]
 for j in range(len(p['topics'])):
  for i,(cat,templ) in enumerate(todos):
   x=p['topics'][(j+i)%len(p['topics'])]
   task=templ.format(x=x)
   seq.append((task,cat,p['profession'],p['sector'],p['sourceGroup'],infer_intent(task,arch)))
 queue.append(seq)
r=0
while len(rows)<50000:
 progress=0
 for seq in queue:
  if r<len(seq):
   task,cat,prof,sec,src,intent=seq[r]
   progress+=push(task,cat,prof,sec,src,intent,[],'contextual')
   if len(rows)==50000:break
 r+=1
 if r>max(map(len,queue)):raise RuntimeError(f'Apenas {len(rows)} casos; não há templates suficientes')
# Tarefas básicas: substituição de 30 entradas contextuais sem inflar 50.000.
# Sinônimos são aliases, não novos casos de uso.
BASIC_SUMMARIES = json.loads("[[\"Resumir texto\",\"routine\",\"everyday\",\"openai2025\",[\"resumir um texto\",\"resumir esse texto\",\"resumir este texto\",\"resuma esse texto\",\"resuma este texto\",\"fazer resumo de texto\",\"fazer um resumo\",\"resumo de texto\",\"sintetizar texto\",\"sumarizar texto\",\"summarize text\",\"summarize this text\",\"summarise text\",\"sintese de texto\"]],[\"Resumir e-mail\",\"routine\",\"email\",\"openai2025\",[\"resumir email\",\"resumir um e-mail\",\"resumir um email\",\"resumir meus emails\",\"resumir emails\",\"resumo de email\",\"resumo de e-mail\",\"resumir email recebido\",\"resumir e-mail recebido\",\"resumir o email que recebi\",\"sumarizar email\",\"summarize email\",\"summarize an email\",\"summarize this email\"]],[\"Resumir um PDF\",\"routine\",\"files\",\"openai2025\",[\"resumir pdf\",\"fazer resumo pdf\",\"summarize pdf\",\"resumir arquivo pdf\"]],[\"Resumir um documento do Word\",\"routine\",\"office\",\"openai2025\",[\"resumir documento word\",\"resumir arquivo docx\",\"summarize word document\"]],[\"Resumir uma conversa no WhatsApp\",\"routine\",\"everyday\",\"openai2025\",[\"resumir whatsapp\",\"resumir chat whatsapp\",\"resumo de conversa whatsapp\",\"summarize whatsapp chat\"]],[\"Resumir um vídeo do YouTube\",\"routine\",\"everyday\",\"openai2025\",[\"resumir video\",\"resumir youtube\",\"resumir um video\",\"summarize youtube video\"]],[\"Resumir um podcast\",\"routine\",\"everyday\",\"openai2025\",[\"resumo podcast\",\"resumir episodio podcast\",\"summarize podcast\"]],[\"Resumir mensagens no Slack\",\"routine\",\"office\",\"openai2025\",[\"resumir slack\",\"resumir conversa do slack\",\"slack summary\"]],[\"Resumir mensagens no Teams\",\"routine\",\"office\",\"openai2025\",[\"resumir conversa teams\",\"resumo de chat teams\",\"summarize teams chat\"]],[\"Resumir uma página da internet\",\"routine\",\"everyday\",\"openai2025\",[\"resumir site\",\"resumir pagina web\",\"resumir link\",\"summarize webpage\"]],[\"Resumir um livro\",\"routine\",\"everyday\",\"openai2025\",[\"resumir livro\",\"resumo de livro\",\"book summary\"]],[\"Resumir um capítulo de livro\",\"routine\",\"everyday\",\"openai2025\",[\"resumir capitulo\",\"resumo de capitulo\",\"summarize book chapter\"]],[\"Resumir um relatório de trabalho\",\"routine\",\"office\",\"openai2025\",[\"resumir relatorio\",\"sumarizar relatorio\",\"summarize work report\"]],[\"Resumir anotações de reunião\",\"routine\",\"office\",\"openai2025\",[\"resumir notas de reuniao\",\"resumo de reuniao\",\"summarize meeting notes\"]],[\"Resumir uma gravação de áudio\",\"routine\",\"everyday\",\"openai2025\",[\"resumir audio\",\"resumo de audio\",\"summarize audio recording\"]],[\"Resumir uma apresentação PowerPoint\",\"routine\",\"office\",\"openai2025\",[\"resumir powerpoint\",\"resumir slides\",\"summarize slides\"]],[\"Resumir um contrato em linguagem simples\",\"routine\",\"legal\",\"thomson2025\",[\"resumir contrato\",\"resumo contrato\",\"explicar contrato em poucas palavras\"]],[\"Resumir um artigo científico\",\"routine\",\"research\",\"research2025\",[\"resumir paper\",\"resumir estudo cientifico\",\"summarize research paper\"]],[\"Resumir um manual técnico\",\"routine\",\"engineering\",\"anthropic2026\",[\"resumir manual\",\"resumo manual tecnico\",\"summarize technical manual\"]],[\"Resumir um edital\",\"routine\",\"office\",\"openai2025\",[\"resumir edital\",\"resumo edital\",\"summarize public notice\"]],[\"Resumir uma conversa de suporte ao cliente\",\"routine\",\"business\",\"openai2025\",[\"resumir conversa atendimento\",\"resumir chat atendimento\"]],[\"Resumir uma notícia\",\"routine\",\"everyday\",\"openai2025\",[\"resumir noticia\",\"resumo da noticia\",\"summarize news article\"]],[\"Resumir uma transcrição de entrevista\",\"routine\",\"office\",\"openai2025\",[\"resumir entrevista\",\"resumir transcricao\",\"summarize interview transcript\"]],[\"Resumir uma conversa em grupo\",\"routine\",\"everyday\",\"openai2025\",[\"resumir conversa de grupo\",\"resumir grupo de mensagens\"]],[\"Resumir e-mails não lidos\",\"routine\",\"email\",\"openai2025\",[\"resumir caixa de entrada\",\"resumir inbox\",\"resumo emails nao lidos\"]],[\"Resumir comentários de clientes\",\"routine\",\"business\",\"openai2025\",[\"resumir feedback clientes\",\"resumir avaliacoes clientes\"]],[\"Resumir orientações de um curso\",\"learn\",\"education\",\"openai2025\",[\"resumir materia para estudar\",\"resumir texto para prova\",\"resumir aula para estudar\"]],[\"Resumir texto jurídico para compreensão\",\"routine\",\"legal\",\"thomson2025\",[\"resumir lei\",\"resumir documento juridico\",\"simplificar juridiquês\"]],[\"Resumir dados de uma pesquisa\",\"routine\",\"research\",\"research2025\",[\"resumir resultados de pesquisa\",\"sumarizar dados experimento\"]],[\"Resumir um documento longo\",\"routine\",\"files\",\"openai2025\",[\"resumir documento\",\"resumo de documento\",\"summarize a long document\"]]]")
assert len(BASIC_SUMMARIES)==30
for row,(title,category,intent,source,aliases) in zip(rows[4970:5000],BASIC_SUMMARIES):
    if norm(title) in seen:raise ValueError('Tarefa básica duplicada: '+title)
    seen.discard(norm(row['task']))
    seen.add(norm(title))
    if intent=='research':prof,sec='Pesquisador','Ciência e pesquisa'
    elif intent=='legal':prof,sec='Pessoas em geral','Vida cotidiana'
    elif intent=='engineering':prof,sec='Engenheiro','Engenharia'
    elif intent=='education':prof,sec='Pessoas em geral','Educação'
    elif intent in ('email','office','business'):prof,sec='Profissional administrativo','Escritório e comunicação'
    else:prof,sec='Pessoas em geral','Vida cotidiana'
    row.update(task=title,category=category,profession=prof,sector=sec,sourceGroup=source,intent=intent,priority='essencial',aliases=aliases)
assert len(rows)==50000
assert len(set(norm(x['task']) for x in rows))==50000
# Índice de aliases separate from count, prefer meaningful anchors in ranking.
assert len([x for x in rows if x['intent']=='email'])>250
assert len([x for x in rows if x['intent']=='photos'])>130
assert len([x for x in rows if x['intent']=='research'])>1000
assert len(set(x['profession'] for x in rows))>=198
CATS=sorted(set(x['category'] for x in rows));PROFS=sorted(set(x['profession'] for x in rows));SECTS=sorted(set(x['sector'] for x in rows));SOURCES=sorted(set(x['sourceGroup'] for x in rows));INTENTS=sorted(set(x['intent'] for x in rows))
mapidx=lambda xs:{x:i for i,x in enumerate(xs)}
ci,pi,si,soi,ii=mapidx(CATS),mapidx(PROFS),mapidx(SECTS),mapidx(SOURCES),mapidx(INTENTS)
# Catalog entries: [id,task,category#,profession#,sector#,source#,intent#,priorityFlag,aliases?]
# Contexts are real scenarios, not directly observed frequency rankings.
packed=[]
for x in rows:
 packed.append([x['id'],x['task'],ci[x['category']],pi[x['profession']],si[x['sector']],soi[x['sourceGroup']],ii[x['intent']],1 if x['priority']=='essencial' else 0, x['aliases'] or None])
header='/* Editorial scenarios: 50,000 contextual examples, not a frequency ranking. */\n'
loader='''/* Locally unpack task shards; no network calls to AI models. */\n(()=>{\nconst d=window.UYB_DICTIONARIES;\nwindow.ANTES_TASKS=(window.UYB_PACKED||[]).map(r=>({id:r[0],task:r[1],category:d.categories[r[2]],profession:d.professions[r[3]],sector:d.sectors[r[4]],sourceGroup:d.sources[r[5]],intent:d.intents[r[6]],priority:r[7]?'essencial':'contextual',aliases:r[8]||[]}));\nwindow.UYB_READY=window.ANTES_TASKS.length===50000;\nwindow.UYB_PACKED=null;\n})();\n'''
(ROOT/'catalogo-loader.js').write_text('window.UYB_DICTIONARIES='+json.dumps({'categories':CATS,'professions':PROFS,'sectors':SECTS,'sources':SOURCES,'intents':INTENTS},ensure_ascii=False,separators=(',',':'))+';\n'+loader,encoding='utf-8')
for shard in range(10):
 subset=packed[shard*5000:(shard+1)*5000]
 txt=header+('window.UYB_PACKED=window.UYB_PACKED||[];\n' if shard==0 else '')+'window.UYB_PACKED.push(...'+json.dumps(subset,ensure_ascii=False,separators=(',',':'))+');\n'
 # spread argument list of 5000 below JS 65535 argument limit.
 (ROOT/f'catalogo/parte-{shard:02d}.js').write_text(txt,encoding='utf-8')
with (ROOT/'data/catalogo-50000.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=['id','task','category','profession','sector','sourceGroup','intent','priority','aliases']);wr.writeheader()
 for x in rows:wr.writerow({**x,'aliases':' | '.join(x['aliases'])})
(ROOT/'data/catalogo-50000.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Entradas:',len(rows),'Âncoras:',len(ANCHORS),'Profissões:',len(set(x['profession'] for x in rows)),'Setores:',len(set(x['sector'] for x in rows)))
print('Intents:',Counter(x['intent'] for x in rows))
print('Categorias:',Counter(x['category'] for x in rows))
print('Tamanhos shards',[round((ROOT/f'catalogo/parte-{i:02d}.js').stat().st_size/1024) for i in range(10)])
for t in ['Escrever um e-mail profissional','Responder a um e-mail recebido','Organizar minhas fotos do Google Fotos','Organizar pastas no computador','Buscar artigos científicos no PubMed','Escrever minha tese de doutorado']:
 print('Anchor',t,any(x['task']==t for x in rows))