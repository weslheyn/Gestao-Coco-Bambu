/**
 * Regras de OCR para o nome do colaborador.
 * Módulo isolado para homologação; NÃO conectado ao bot em produção.
 * Não extrair dados pessoais além do nome necessário ao recibo.
 */
export const INSTRUCOES_NOME_OCR = [
  "Antes de retornar o nome, leia independentemente as três regiões do recibo:",
  "(1) campo Nome manuscrito, (2) campo Assinatura, (3) nome impresso no documento anexado.",
  "Compare o primeiro nome e cada sobrenome entre as três fontes.",
  "Se o documento impresso estiver legível e corresponder ao nome manuscrito,",
  "use a grafia do documento para resolver ambiguidades da escrita manual.",
  "Assinaturas podem ser rubricas: quando ilegíveis, não invente letras ou sobrenomes.",
  "Se as fontes divergirem e não for possível confirmar a mesma pessoa com segurança,",
  "retorne nome:null para conferência humana, sem inventar nem escolher ao acaso.",
  "Não leia nem retorne CPF, RG, endereço, filiação, nascimento ou dados do documento além do nome.",
  "Para data_servico, use apenas a data do campo Serviço no recibo; ignore datas do documento.",
  "Preserve o formato de saída JSON já esperado pela função e os outros campos do recibo."
].join(" ");

/** Casos de homologação; exemplos sintéticos, sem dados pessoais de documento. */
export const CASOS_DE_TESTE_NOME_OCR = [
  {
    caso: "recibo-6827",
    descricao: "Nome manuscrito ambíguo; documento impresso legível; assinatura rubrica",
    esperado: { nome: "Iris Laurentino Martins Nunes", data_servico: "2026-09-21", valor: 80 },
  },
  {
    caso: "rubrica-sem-documento-legivel",
    descricao: "Nome ilegível, assinatura rubrica e documento ilegível",
    esperado: { nome: null },
  },
  {
    caso: "documento-divergente",
    descricao: "Nome do documento não corresponde ao nome manuscrito; vínculo incerto",
    esperado: { nome: null },
  },
] as const;
