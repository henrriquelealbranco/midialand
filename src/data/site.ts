export const site = {
  name: 'Midialand',
  tagline: 'Mídia que encontra a vida.',
  whatsappEnabled: false,
  formDeliveryEnabled: false,
};

export const navigation = [
  { href: '/produtos/', label: 'Soluções' },
  { href: '/onde-estamos/', label: 'Onde estamos' },
  { href: '/cases/', label: 'Campanhas' },
  { href: '/sobre-nos/', label: 'A Midialand' },
  { href: '/blog/', label: 'Conteúdos' },
];

export const offices = [
  {
    city: 'Curitiba',
    state: 'PR',
    address: 'Rod. Curitiba-Ponta Grossa BR-277, 1912',
    neighborhood: 'Santo Inácio · CEP 82305-100',
    phone: '(41) 3263-1707',
    href: 'tel:+554132631707',
  },
  {
    city: 'Porto Alegre',
    state: 'RS',
    address: 'Rua Álvaro Chaves, 321',
    neighborhood: 'Floresta · CEP 90220-040',
    phone: '(51) 3307-1832',
    href: 'tel:+555133071832',
  },
];

export const socials = [
  { name: 'Instagram', href: 'https://www.instagram.com/midialand_/' },
  { name: 'LinkedIn', href: 'https://www.linkedin.com/company/midialand' },
  { name: 'Facebook', href: 'https://www.facebook.com/midialandooh' },
];

export interface Solution {
  id: string;
  title: string;
  short: string;
  description: string;
  image: string;
  alt: string;
  tag: string;
  applications: string[];
  coverage: string;
}

export const solutions: Solution[] = [
  {
    id: 'grandes-formatos',
    title: 'Grandes formatos',
    short: 'Presença que muda a paisagem.',
    description:
      'Painéis estáticos e empenas levam a mensagem da sua marca para as ruas, avenidas e trajetos rodoviários. Uma presença visual que participa do dia a dia da cidade.',
    image: 'estatico',
    alt: 'Painel publicitário vertical junto a uma avenida com fluxo de veículos',
    tag: 'Mídia exterior · OOH',
    applications: [
      'Campanhas institucionais',
      'Lançamentos de produtos',
      'Comunicação em trajetos urbanos',
    ],
    coverage:
      'Curitiba, São José dos Pinhais e Porto Alegre. Consulte também as possibilidades no Paraná.',
  },
  {
    id: 'paineis-digitais',
    title: 'Painéis digitais',
    short: 'Sua mensagem no ritmo da cidade.',
    description:
      'Telas de LED dão movimento à comunicação em pontos urbanos. O formato permite explorar diferentes peças e narrativas visuais conforme o planejamento da campanha.',
    image: 'digital',
    alt: 'Painel digital de LED acima de uma via urbana movimentada',
    tag: 'Mídia digital · DOOH',
    applications: [
      'Peças em movimento',
      'Campanhas sazonais',
      'Diferentes mensagens de uma mesma marca',
    ],
    coverage: 'Curitiba, São José dos Pinhais e Porto Alegre. Pontos e condições sob consulta.',
  },
  {
    id: 'transporte-coletivo',
    title: 'Mídia no transporte',
    short: 'Parte de cada ida e volta.',
    description:
      'TVs no interior dos ônibus e nos terminais aproximam a comunicação dos trajetos cotidianos. Formatos que acompanham momentos de deslocamento e espera.',
    image: 'onibus',
    alt: 'Passageiro em pé no ônibus próximo a uma tela de publicidade',
    tag: 'Ônibus e estações',
    applications: [
      'Comunicação durante os trajetos',
      'Conteúdo audiovisual',
      'Campanhas em circuitos de transporte',
    ],
    coverage: 'Transporte coletivo de Curitiba. Consulte os circuitos com a equipe.',
  },
  {
    id: 'mobiliario-urbano',
    title: 'Mobiliário urbano',
    short: 'Perto de quem está passando.',
    description:
      'MUBs e estruturas de mídia integram a comunicação aos espaços de circulação. Nos terminais, a mensagem encontra as pessoas em seus percursos pela cidade.',
    image: 'mobiliario',
    alt: 'Equipamento de mídia vertical entre passageiros em um terminal',
    tag: 'MUBs e espaços urbanos',
    applications: [
      'Presença nos terminais',
      'Comunicação de proximidade',
      'Complemento a campanhas em outros formatos',
    ],
    coverage: 'MUBs em terminais de Curitiba. Demais formatos e praças sob consulta.',
  },
  {
    id: 'projetos-e-ativacoes',
    title: 'Projetos e ativações',
    short: 'Da mensagem ao encontro.',
    description:
      'Experiências presenciais e projetos especiais criam outras maneiras de apresentar uma marca. A proposta é desenhada com a equipe, a partir da ideia e do espaço disponível.',
    image: 'ativacao',
    alt: 'Ativação de marca com estrutura interativa e participante em terminal de ônibus',
    tag: 'Experiências de marca',
    applications: [
      'Ativações nos terminais',
      'Experiências presenciais',
      'Projetos especiais de comunicação',
    ],
    coverage: 'Ativações em terminais de Curitiba. Outros projetos conforme avaliação da equipe.',
  },
];

export const cities = [
  {
    id: 'curitiba',
    name: 'Curitiba',
    state: 'Paraná',
    description:
      'Das avenidas aos trajetos de ônibus, diferentes formatos para fazer parte da rotina da capital.',
    formats: ['Painéis estáticos', 'Painéis digitais', 'Transporte coletivo', 'Ativações'],
    document: 'INVENTARIO_painel_CWB.pdf',
    office: offices[0],
    contactNote: 'Fale com a equipe de Curitiba',
  },
  {
    id: 'sao-jose-dos-pinhais',
    name: 'São José dos Pinhais',
    state: 'Paraná',
    description:
      'Grandes formatos e mídia digital nos caminhos da Região Metropolitana de Curitiba.',
    formats: ['Painéis estáticos', 'Painéis digitais'],
    document: 'INVENTARIO_painel_SJP.pdf',
    office: offices[0],
    contactNote: 'Atendimento pela equipe de Curitiba',
  },
  {
    id: 'porto-alegre',
    name: 'Porto Alegre',
    state: 'Rio Grande do Sul',
    description:
      'Mídia exterior e painéis digitais para conectar a sua mensagem aos percursos da capital gaúcha.',
    formats: ['Painéis estáticos', 'Painéis digitais'],
    document: 'INVENTARIO_painel_POA.pdf',
    office: offices[1],
    contactNote: 'Fale com a equipe de Porto Alegre',
  },
];

export type GalleryCategory = 'Grandes formatos' | 'Mídia digital' | 'Transporte' | 'Ativações';
export interface GalleryItem {
  image: string;
  title: string;
  category: GalleryCategory;
  alt: string;
}
export const gallery: GalleryItem[] = [
  {
    image: 'galeria-painel',
    title: 'A cidade como ponto de encontro',
    category: 'Grandes formatos',
    alt: 'Painel horizontal com aplicação tridimensional acima de um muro com grafites e uma avenida',
  },
  {
    image: 'galeria-digital',
    title: 'Uma mensagem em movimento',
    category: 'Mídia digital',
    alt: 'Painel digital com anúncio de fundo vermelho ao lado de uma rua urbana',
  },
  {
    image: 'galeria-terminal',
    title: 'Entre chegadas e partidas',
    category: 'Transporte',
    alt: 'Passageiros caminhando em terminal com telas suspensas de comunicação',
  },
  {
    image: 'galeria-rodovia',
    title: 'Presença ao longo do caminho',
    category: 'Grandes formatos',
    alt: 'Painel de grande formato em área verde ao lado de uma rodovia',
  },
  {
    image: 'galeria-mub',
    title: 'A comunicação mais próxima',
    category: 'Transporte',
    alt: 'Mobiliário de mídia digital vertical em plataforma de terminal de ônibus',
  },
  {
    image: 'ativacao',
    title: 'Uma ideia que vira experiência',
    category: 'Ativações',
    alt: 'Pessoa participando de uma ativação de marca com bola e estrutura temática em terminal',
  },
  {
    image: 'galeria-urbana',
    title: 'No cotidiano de quem circula',
    category: 'Grandes formatos',
    alt: 'Grande painel publicitário entre edifícios em uma avenida com automóveis',
  },
  {
    image: 'onibus',
    title: 'Companhia em cada trajeto',
    category: 'Transporte',
    alt: 'Passageiro no interior de ônibus com uma TV publicitária à sua frente',
  },
];

export const articles = [
  {
    title: 'Quando a marca vira experiência no terminal',
    date: '2026-06-11',
    displayDate: '11 de junho de 2026',
    category: 'Experiências de marca',
    image: 'ativacao',
    alt: 'Ativação interativa de marca em um terminal de ônibus',
    summary:
      'Uma aproximação que acontece ao vivo: a publicação apresenta possibilidades de ativação de marca nos terminais de Curitiba.',
    href: 'https://midialand.com/ativacao-de-marca-em-curitiba/',
  },
  {
    title: 'Novas ideias para uma cidade mais sustentável',
    date: '2026-05-12',
    displayDate: '12 de maio de 2026',
    category: 'Cidade e sustentabilidade',
    image: 'hackathon',
    alt: 'Grupo de participantes reunidos durante o hackathon da Unisinos',
    summary:
      'O encontro com estudantes da Unisinos, em Porto Alegre, abriu espaço para pensar soluções sustentáveis. A publicação prevê a execução da proposta vencedora.',
    href: 'https://midialand.com/hackathon-em-porto-alegre-unisinos-solucoes-sustentaveis/',
  },
];

export const routes = [
  '/',
  '/produtos/',
  '/tv-do-onibus/',
  '/onde-estamos/',
  '/cases/',
  '/sobre-nos/',
  '/blog/',
  '/contato/',
];
