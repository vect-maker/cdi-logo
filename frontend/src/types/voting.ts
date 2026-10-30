export interface CandidateFigure {
  id: string
  slot: string
  name: string
  subtitle: string
  svgPath: (palette: string) => string
}

export interface ColorPalette {
  id: string
  name: string
  primaryHex: string
  secondaryHex: string
}

export interface CompositionType {
  id: 'symbols' | 'lockups' | 'stacked'
  name: string
  subtitle: string
  getAssetFilename: (palette: string) => string
}

export interface FabricColor {
  id: 'black' | 'charcoal' | 'gray'
  name: string
  hex: string
}

export interface StudentVote {
  round: string
  studentCode: string
  figureId: string
  paletteId: string
  compositionId: 'symbols' | 'lockups' | 'stacked'
  recommendations: string
  timestamp: number
  isoDate: string
}

export const CANDIDATE_FIGURES: CandidateFigure[] = [
  {
    id: 'c1-neural',
    slot: '01',
    name: 'Neural Cluster',
    subtitle: 'Redes y nodos de datos',
    svgPath: (palette) => `/candidates/c1-neural/symbols/symbol-${palette}.svg`,
  },
  {
    id: 'c2-matrix',
    slot: '02',
    name: 'Matrix Tensor',
    subtitle: 'Estructura isométrica matricial',
    svgPath: (palette) => `/candidates/c2-matrix/symbols/symbol-${palette}.svg`,
  },
  {
    id: 'c3-hexcore',
    slot: '03',
    name: 'Hex Data Core',
    subtitle: 'Núcleo de datos hexagonal',
    svgPath: (palette) => `/candidates/c3-hexcore/symbols/symbol-${palette}.svg`,
  },
  {
    id: 'c4-tesseract',
    slot: '04',
    name: '4D Hypercube Tesseract',
    subtitle: 'Proyección geométrica de hipercubo',
    svgPath: (palette) => `/candidates/c4-tesseract/symbols/symbol-${palette}.svg`,
  },
  {
    id: 'c5-voronoi',
    slot: '05',
    name: 'Voronoi Decision Cells',
    subtitle: 'Células y fronteras Voronoi',
    svgPath: (palette) => `/candidates/c5-voronoi/symbols/symbol-${palette}.svg`,
  },
  {
    id: 'c6-waveform',
    slot: '06',
    name: 'Harmonized Waveform',
    subtitle: 'Onda armónica de datos',
    svgPath: (palette) => `/candidates/c6-waveform/symbols/symbol-${palette}.svg`,
  },
]

export const COLOR_PALETTES: ColorPalette[] = [
  {
    id: 'cobalt',
    name: 'Azul & Cian',
    primaryHex: '#3B82F6',
    secondaryHex: '#00F0FF',
  },
  {
    id: 'emerald',
    name: 'Esmeralda & Menta',
    primaryHex: '#10B981',
    secondaryHex: '#00F5D4',
  },
  {
    id: 'violet',
    name: 'Violeta & Fucsia',
    primaryHex: '#8B5CF6',
    secondaryHex: '#FF2A85',
  },
  {
    id: 'amber',
    name: 'Ámbar & Naranja',
    primaryHex: '#F59E0B',
    secondaryHex: '#FF5400',
  },
]

export const COMPOSITION_TYPES: CompositionType[] = [
  {
    id: 'symbols',
    name: 'Símbolo Solo',
    subtitle: 'Isotipo sin texto',
    getAssetFilename: (palette) => `symbols/symbol-${palette}.svg`,
  },
  {
    id: 'lockups',
    name: 'Logo Horizontal',
    subtitle: 'Símbolo y texto en línea',
    getAssetFilename: (palette) => `lockups/lockup-${palette}.svg`,
  },
  {
    id: 'stacked',
    name: 'Logo Centrado',
    subtitle: 'Símbolo arriba y texto abajo',
    getAssetFilename: (palette) => `stacked/stacked-${palette}.svg`,
  },
]

export const FABRIC_COLORS: FabricColor[] = [
  {
    id: 'black',
    name: 'Negro',
    hex: '#111827',
  },
  {
    id: 'charcoal',
    name: 'Carbón',
    hex: '#374151',
  },
  {
    id: 'gray',
    name: 'Gris Jaspe',
    hex: '#9CA3AF',
  },
]
