# Conferência de nomes em recibos — Caixa (proposta para homologação)

**Situação:** proposta isolada, não publicada no bot. Produção permanece na função `telegram-caixa` v67.

## Regras
1. Ler separadamente: (a) campo **Nome** manuscrito, (b) campo **Assinatura**, (c) nome impresso no documento de identificação anexado.
2. Comparar primeiro nome e sobrenomes. Se o documento impresso estiver legível e corresponder à pessoa do recibo, usá-lo como referência para grafia; não usar uma assinatura ilegível/rubrica para inventar letras.
3. Se houver divergência que não possa ser resolvida com segurança, retornar `nome: null` e encaminhar para **conferência manual**, sem atribuir um nome por suposição.
4. Não extrair nem armazenar números do documento, filiação, endereço, data de nascimento ou outras informações pessoais do documento.
5. `data_servico` deve vir **somente** do campo de data do serviço do recibo; não usar datas do documento de identificação.
6. Preservar extração de recibo, valor, PAGO, verificação de duplicidade, armazenamento de imagem, botões de edição/exclusão e todos os fluxos já existentes.

## Caso de teste
- Recibo **6827**: nome correto **Iris Laurentino Martins Nunes**; não interpretar como “Luis”.
- Assinatura é uma rubrica: não inferir grafia a partir dela.
- Data do serviço: **21/09/2026**, indicada no quadro Serviço.
- Valor: **R$ 80,00**.
- Confirmar que não são extraídos dados sensíveis do documento.

## Critérios de aprovação
- Três fontes avaliadas independentemente e comparadas antes da consolidação.
- Resultado incerto gera pendência de conferência, não nome presumido.
- Fluxos de Freelance, Dobra, Folga e Vale mantidos.
- Testes com recibos reais autorizados antes de qualquer deploy.

**Nota técnica:** a Edge Function contém integrações e segredos referenciados no ambiente Supabase. Não copiar o código de produção para este repositório público sem revisão de segurança.
