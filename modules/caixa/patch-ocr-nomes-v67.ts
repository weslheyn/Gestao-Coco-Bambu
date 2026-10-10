/** Patch de homologação para telegram-caixa v67. Não realiza deploy. */
const atual = 'Retorne um único nome completo consolidado com a grafia mais confiável pela concordância entre as fontes.';
const revisado = 'Antes de consolidar o nome, analise SEPARADAMENTE as três fontes da MESMA pessoa: campo Nome manuscrito, campo Assinatura e nome impresso no documento anexado. Compare o primeiro nome e cada sobrenome. Quando o documento impresso estiver legível e corresponder ao colaborador do recibo, utilize sua grafia para resolver ambiguidades do manuscrito. Uma assinatura que seja apenas rubrica não serve para inferir letras. Se as fontes forem conflitantes ou insuficientes, retorne nome:null para conferência manual; nunca invente um nome. Retorne um único nome completo somente quando a grafia estiver sustentada pelas fontes.';
export function aplicarAjusteNomeOCR(codigoFonte: string): string {
  const inicio = codigoFonte.indexOf('async function extrairRecibo(');
  const fim = codigoFonte.indexOf('async function extrairVale(', inicio);
  if (inicio < 0 || fim < 0) throw new Error('Funções esperadas não encontradas');
  const trecho = codigoFonte.slice(inicio, fim);
  if (trecho.split(atual).length !== 2) throw new Error('Prompt original divergente: não alterar');
  return codigoFonte.slice(0, inicio) + trecho.replace(atual, revisado) + codigoFonte.slice(fim);
}
