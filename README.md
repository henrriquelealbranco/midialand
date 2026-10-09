# Midialand — proposta de site

Site institucional e comercial completo em português brasileiro, executado localmente. **Não publicado.** As páginas são geradas em HTML estático por Astro, com TypeScript para dados e interações.

## Executar

Requisitos: Node.js 24.16 ou superior (a revisão utilizou 24.19.0) e npm.

```powershell
git clone https://github.com/henrriquelealbranco/midialand.git
cd midialand
npm ci
npm run dev
```

Abra **http://127.0.0.1:4321/**. O servidor fica restrito ao computador local.

Para reproduzir a versão compilada:

```powershell
npm run lint
npm run build
npm run preview
```

Não execute `dev` e `preview` na mesma porta simultaneamente. A pasta `dist/` contém a versão estática. Não há banco, login, painel administrativo nem servidor de recebimento de contatos.

## Páginas e rotas

| URL | Conteúdo |
| --- | --- |
| `/` | Apresentação, soluções, praças, galeria, transporte, iniciativas e contato |
| `/produtos/` | Cinco formatos com aplicações, praças, mídia kit e CTA contextual |
| `/tv-do-onibus/` | Ônibus, TVs Estações, MUBs e ativações |
| `/onde-estamos/` | Três praças, inventários e contatos |
| `/cases/` | Oito fotografias, filtros de formato e lightbox |
| `/sobre-nos/` | Atuação, Jardim Pugsley e contexto do hackathon |
| `/blog/` | Dois resumos originais com data e link para a publicação oficial |
| `/contato/` | Jornadas “Quero anunciar” e “Quero ceder espaço” |

As seis rotas antigas exigidas pelo briefing foram preservadas. Nenhuma dessas rotas precisa de redirecionamento. A nova rota é `/onde-estamos/`. A hospedagem futura deve normalizar URLs sem barra final para a equivalente com barra e usar `404.html` para endereços inexistentes. Os artigos completos continuam no site oficial; não foram reproduzidos nem migrados.

## Organização

- `src/data/site.ts`: conteúdo tipado, contatos, soluções, cidades, galeria e artigos.
- `src/data/images.json`: dimensões e variantes de cada fotografia, origem e páginas de referência.
- `src/components/`: fotografias responsivas, cidades, galeria, artigos e formulário.
- `src/layouts/Layout.astro`: header, menu, metadados, chamada final e rodapé.
- `src/scripts/`: interações pequenas em TypeScript; foco de modais compartilhado.
- `src/styles/global.css`: tokens e estilos responsivos, organizados em camadas.
- `public/images/`: derivados WebP e cópias das logos originais.
- `public/downloads/`: cinco PDFs locais de referência.
- `scripts/prepare_assets.py`: geração reproduzível dos derivados.
- `scripts/test_site.py`: testes de navegação e acessibilidade automatizada.
- `review/`: capturas, auditoria do material e resultados dos testes.
- `docs/IMAGENS.md`: lista das imagens escolhidas com suas origens.
- `docs/PLANO.md`: direção visual e escopo de implementação.

O pacote foi localizado no ZIP fornecido e extraído em `../midialand-kit`. Os originais foram preservados e os 185 hashes do manifesto conferiram. O catálogo foi aberto no navegador e as fotografias foram inspecionadas antes da seleção. Os cinco PDFs foram lidos como documentos históricos, sem converter seus números em inventário vigente.

O repositório já inclui as imagens otimizadas, as logos e os PDFs necessários para executar e compilar o site. O ZIP e a pasta original `midialand-kit` não são necessários para `npm run dev` ou `npm run build`; são necessários apenas para regenerar imagens com `npm run assets` ou repetir a auditoria do material. Nesse caso, extraia o kit ao lado da pasta clonada. Capturas e arquivos temporários de revisão permanecem locais e são recriados pelos testes; os relatórios JSON estão versionados.

## Design e conteúdo

A direção preserva o coral `#EC684A`, o roxo `#432459` e as logos originais. O roxo sustenta textos e botões; o coral funciona como acento. A abertura combina tipografia forte e fotografia urbana sem sobrepor a leitura às mensagens presentes nos painéis. Seções fotográficas, blocos claros e áreas roxas criam variação entre os assuntos.

Manrope variável é servida localmente pelo pacote `@fontsource-variable/manrope`, licença SIL Open Font License 1.1. A licença também acompanha o projeto em `docs/MANROPE-LICENSE.txt`. Nenhum arquivo Gotham foi utilizado. O texto de abertura e “Mídia que encontra a vida” são propostas editoriais, não slogans oficiais confirmados.

Não foram incluídos números de impacto ou inventário, resultados, depoimentos, nomes de clientes inferidos, fundação, porte ou promessas de disponibilidade. Os filtros da galeria classificam somente o formato visualmente identificável. O hackathon é apresentado como evento, com execução do projeto vencedor prevista no relato; a fotografia não é atribuída ao Jardim Pugsley.

O kit traz três URLs de mapas, mas não relaciona explicitamente cada identificador à cidade correspondente. Para evitar uma associação incorreta, esta proposta usa a seleção de praças, os inventários e os contatos, sem incorporar mapas.

## Formulários e WhatsApp

Os formulários **não enviam dados**, não usam armazenamento local e não possuem endpoint. A validação ocorre no navegador, o primeiro campo inválido recebe foco, e o resumo é produzido com texto literal. O visitante pode copiar esse resumo. Se o navegador negar a área de transferência, o texto fica selecionado e a interface explica como copiar manualmente.

Os links de produtos e praças preenchem a solução/cidade apenas quando o parâmetro corresponde a uma opção conhecida. Telefone é opcional na jornada de anúncio. A jornada de espaço aceita e-mail ou telefone como contato.

Para conectar um destino real depois da autorização:

1. Confirmar destinatário comercial, provedor e regras de tratamento dos dados com a Midialand. O e-mail citado no material ainda não foi validado como destino de leads.
2. Definir um endpoint próprio ou serviço autorizado, com validação no servidor, proteção contra abuso e segredos fora do navegador. Nunca colocar credenciais no código público.
3. Substituir a geração de demonstração em `src/scripts/contact.ts` pela chamada a esse destino, mantendo feedback de erro e os valores em caso de falha. Só apresentar confirmação após resposta real de sucesso.
4. Atualizar aviso, botão e política de privacidade com o texto efetivamente aprovado. Testar falha, indisponibilidade, duplicidade e entrega antes de ativar.

O WhatsApp está desativado porque os números publicados divergem. `site.whatsappEnabled` e `site.formDeliveryEnabled` documentam esse estado; alterar esses campos não cria uma integração. Não há chat flutuante nem abertura automática. Telefones fixos e redes sociais usam os endereços registrados no material.

## Domínio, busca e publicação futura

Por padrão, todas as páginas têm `noindex, nofollow, noarchive` e `robots.txt` bloqueia rastreamento. O sitemap existe e contém as oito rotas. Canonical e Open Graph usam o domínio configurável, cujo padrão é `http://localhost:4321`.

Para compilar futuramente com um domínio **já autorizado**, defina `SITE_URL` no ambiente. Exemplo de sintaxe PowerShell (o domínio abaixo é ilustrativo):

```powershell
$env:SITE_URL = 'https://dominio-confirmado.example'
$env:PUBLIC_ALLOW_INDEXING = 'false'
npm run build
```

Só habilitar `PUBLIC_ALLOW_INDEXING=true` depois da autorização de publicação no domínio correto. A indexação permanece bloqueada em localhost, mesmo com o sinalizador ativo. O `.env.example` documenta os valores, mas `SITE_URL` deve ser definido no ambiente do processo de build. `noindex` não é controle de acesso: uma apresentação remota privada futura precisará de autenticação no ambiente de hospedagem.

Não há publicação ou configuração de deploy nesta entrega. Antes de qualquer publicação, confirmar:

- autorização de uso das fotografias, campanhas e materiais;
- inventários e PDFs vigentes, cobertura e especificações atuais;
- número oficial do WhatsApp e destino dos formulários;
- política de privacidade e tratamento de dados aprovados;
- identidade visual, tipografia, textos editoriais e permissões de marca;
- domínio, redirecionamentos e regras de acesso ao ambiente de apresentação.

## Testes

Com `npm run preview` em outro terminal:

```powershell
python -m pip install -r scripts/requirements.txt
python -m playwright install chromium
npm test
```

O teste usa Chromium, dados fictícios e o endereço local. Verifica as oito páginas em **390, 768 e 1440 px**, ausência de overflow, imagens, H1, metadados, links e downloads; menu, cidades, filtros, lightbox, Tab/Escape e retorno de foco; ambas as jornadas de contato, cópia e fallback; ausência de envios e requisições a terceiros. Axe-core verifica regras WCAG 2 A/AA e 2.1 AA nas páginas desktop/celular e em estados interativos.

As capturas e `review/test-results.json` registram os resultados. `docs/REVISAO.md` resume a revisão final. Teste automatizado e revisão visual não equivalem a certificação de acessibilidade. Não foram realizados testes em aparelhos físicos, Safari/VoiceOver, NVDA ou rede móvel real, nem medição de Core Web Vitals em produção. PDFs históricos conservam o conteúdo e as limitações de acessibilidade dos originais.
