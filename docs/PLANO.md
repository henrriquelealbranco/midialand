# Midialand — plano de implementação

Objetivo: construir e revisar a proposta privada completa, com oito páginas estáticas, sem publicação e sem envio de dados.

Arquitetura: Astro + TypeScript para HTML renderizado na compilação; dados editoriais tipados; componentes compartilhados; JavaScript apenas para menu, seleção de praça, galeria e formulário. Arquivos originais em ../midialand-kit permanecem intactos.

## Direção visual

- Coral #EC684A, roxo #432459, branco #FFFFFF, cinza claro #F4F3F5, texto #29232E e texto secundário #655D6B.
- Manrope variável local, licença OFL: títulos fortes 700/800, leitura 400/500, legendas 600.
- Abertura em composição assimétrica, título à esquerda e fotografia urbana à direita. Os painéis fotografados são protagonistas; textos não serão sobrepostos às mensagens das campanhas.
- Ritmo entre catálogo fotográfico, faixas roxas, blocos brancos e galeria. Soluções variam entre imagem grande e linhas compactas; evitar repetição de cartões.
- Assinatura: o enquadramento urbano se estende além do bloco de texto no hero, como uma janela para a rua. Sem efeitos luminosos, mapas inventados ou gráficos de alcance.

## Etapas

- [x] Conferir manifesto, catálogo, logos, fotografias e cinco PDFs; registrar fontes e selecionar fotografias após inspeção.
- [x] Gerar WebP em larguras 480, 800, 1200 e 1800 (sem ampliar o original), preservar logos e copiar PDFs para downloads locais.
- [x] Construir conteúdo em src/data/site.ts, imagem responsiva em src/components/Photo.astro e layout com navegação, metadados e rodapé em src/layouts/Layout.astro.
- [x] Implementar /, /produtos/, /tv-do-onibus/, /onde-estamos/, /cases/, /sobre-nos/, /blog/ e /contato/. Todas as rotas legadas pedidas são mantidas.
- [x] Implementar cidades com abas e contatos, lightbox com dialog/foco/Escape e filtros por formato apenas em fotografias verificadas.
- [x] Implementar as duas jornadas de contato com validação, foco no primeiro erro, resumo copiável e nenhum envio de rede.
- [x] Gerar canonical configurável, Open Graph, favicon, sitemap e robots sem indexação por padrão.
- [x] Rodar npm run lint, npm run build e testes Playwright: 390/768/1440, links/downloads, menus, teclado, galeria, formulários, erros de console e overflow. Inspecionar capturas e corrigir.
- [x] Registrar instruções, seleção/origem das imagens, testes, limites reais e pendências de publicação no README e docs.

## Regras editoriais

Sem números de alcance/inventário, clientes inferidos, resultados, data de fundação ou disponibilidade. PDFs identificados como materiais de referência sujeitos a atualização. Artigos externos recebem resumo original e data. Jardim Pugsley e hackathon são iniciativas distintas; foto do evento identifica o evento, sem afirmar implantação do projeto vencedor. WhatsApp e entrega de formulários desativados.

## Critério de conclusão

Oito páginas acessíveis diretamente e rastreáveis em HTML, build/lint sem erros, jornadas testadas, revisão visual nas três larguras, servidor local em execução e nenhuma publicação.
