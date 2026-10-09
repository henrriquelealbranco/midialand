# Revisão da proposta Midialand

Revisão concluída em 09/10/2026. Site servido localmente em `http://127.0.0.1:4321/`, sem publicação. O servidor de prévia escuta somente no endereço de loopback do computador.

## Verificações executadas

| Verificação | Resultado |
| --- | --- |
| `npm run lint` — ESLint + Astro/TypeScript | 0 erros, 0 avisos, 0 hints |
| `npm run build` | 8 páginas institucionais + 404, robots e sitemap gerados |
| `npm audit` | 0 vulnerabilidades reportadas |
| Páginas em 390, 768 e 1440 px | 24 verificações aprovadas, sem overflow horizontal ou imagens quebradas |
| Links internos, parâmetros e âncoras | 28 destinos conferidos |
| Downloads | 5 PDFs retornaram HTTP 200 e cabeçalho PDF válido |
| JavaScript | Nenhuma exceção de página ou requisição falha nos fluxos testados |
| Privacidade da demonstração | Nenhuma requisição de envio; 0 requisições de página a terceiros |
| Metadados | Um H1 por página, títulos/descriptions únicos, canonical e Open Graph configurados |
| Indexação | `noindex, nofollow, noarchive`; robots com `Disallow: /`; sitemap com 8 rotas |
| Axe-core | 19 avaliações: 16 páginas/larguras + menu, lightbox e formulário; 0 violações nas regras WCAG 2 A/AA e 2.1 AA avaliadas |

O relatório completo está em `review/test-results.json`. O registro das 24 verificações de páginas está em `review/page-results.json`. Capturas finais: `review/home-1440.png`, `review/home-768.png`, `review/home-390.png` e os equivalentes das demais páginas; menu, lightbox e resumos têm capturas próprias em 390 px.

## Fluxos testados

- Navegação móvel em 390 e 768 px, links, abertura/fechamento, Escape, contenção e retorno de foco.
- Curitiba, São José dos Pinhais e Porto Alegre: troca de abas, seleção por teclado, telefone e PDF correspondente.
- Galeria: todos os cinco filtros, totais de imagens, abertura, imagem anterior/próxima, setas, Tab, Escape e retorno de foco.
- Anúncio: campos obrigatórios, e-mail inválido, telefone opcional, parâmetros de cidade/solução, foco no primeiro erro e resumo literal sem interpretar HTML.
- Cessão de espaço: campos próprios, contato inválido e válido, resumo sem dados da outra jornada.
- Área de transferência: conteúdo copiado conferido, considerando CRLF do Windows, e fallback com seleção manual quando a API é negada.
- Rotas diretas, downloads locais, âncoras, sitemap, robots e resposta 404 para endereço inexistente.

## Revisão visual e correções

As capturas foram revistas no desktop, tablet e celular emulados. Os ajustes realizados durante a revisão foram:

- Enquadramento do painel digital e do MUB para preservar o equipamento fotografado.
- Fotografia do hackathon em proporção mais ampla no tablet para evitar cortar os participantes.
- Proporções da galeria no celular para mostrar melhor os painéis.
- Contenção explícita de Tab nos diálogos: o comportamento nativo permitia uma passagem momentânea do foco para o corpo da página.
- Título do menu móvel, que recebia indevidamente o tamanho dos títulos de seção.
- Foco com contorno duplo para permanecer perceptível em áreas claras e escuras.
- Aviso do formulário ajustado para os telefones “desta página”, válido também na composição móvel.

O Axe deixou uma revisão manual de `aria-controls` no botão do menu, pois o diálogo está inicialmente oculto. Foi conferido que `aria-controls="mobile-menu"` corresponde ao único diálogo `id="mobile-menu"`; os testes abrem esse diálogo, verificam o foco e o fecham. O detalhe está em `review/axe-manual-review.json`.

## Limites e pendências

A revisão foi feita em Chromium por emulação de viewport. Não representa certificação de acessibilidade, teste em aparelho físico, leitura por NVDA/VoiceOver ou medição de Core Web Vitals em produção. Acessibilidade dos PDFs históricos não foi modificada. Os links externos conservam os endereços fornecidos no briefing; não foram acionadas redes sociais, enviados contatos ou feitas propostas reais.

Formulários e WhatsApp continuam sem integração. Publicação, domínio final, permissões de uso, materiais vigentes e textos de privacidade dependem de confirmação da Midialand, conforme o README.
