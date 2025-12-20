"""
Sistema de processamento de mensagens customizável.
Adicione suas próprias regras de resposta aqui.
"""

import re
from typing import Dict, Optional, List
from datetime import datetime

from estrutura import RoboBolsao


class ChatHandler:
    """Gerenciador de lógica de respostas."""
    
    def __init__(self):
        self.conversa_historico = {}
        # Reaproveita mesma base de dados do bot do Telegram
        self.bot = RoboBolsao('motoristas.json')
        
    def processar_mensagem(self, user_id: str, mensagem: str) -> Dict[str, str]:
        """
        Processa mensagem e retorna resposta.
        
        Args:
            user_id: ID do usuário
            mensagem: Mensagem recebida
            
        Returns:
            Dict com tipo de resposta e texto
        """
        mensagem_original = mensagem.strip()
        mensagem = mensagem_original.lower()
        
        # Salva no histórico
        if user_id not in self.conversa_historico:
            self.conversa_historico[user_id] = []
        self.conversa_historico[user_id].append({
            'texto': mensagem,
            'timestamp': datetime.now().isoformat()
        })
        
        # ============================================
        # ADICIONE SUAS REGRAS CUSTOMIZADAS AQUI! 📝
        # ============================================
        
        # Comandos com /
        if mensagem.startswith('/'):
            return self._processar_comando(mensagem_original)

        # Comandos básicos (mantidos)
        if mensagem in ['oi', 'olá', 'ola', 'hey', 'e ai']:
            return {
                'tipo': 'saudacao',
                'texto': f'Olá! 👋 Como posso ajudar você?'
            }
        
        if mensagem in ['tchau', 'até logo', 'ate logo', 'bye']:
            return {
                'tipo': 'despedida',
                'texto': 'Até logo! 👋 Volte sempre!'
            }
        
        # Perguntas sobre horário
        if 'que horas' in mensagem or 'hora' in mensagem:
            agora = datetime.now()
            return {
                'tipo': 'hora',
                'texto': f'🕐 Agora são {agora.strftime("%H:%M:%S")}\n'
                         f'📅 {agora.strftime("%d/%m/%Y")}'
            }
        
        # Resposta padrão
        return {
            'tipo': 'padrao',
            'texto': f'Recebi sua mensagem: "{mensagem_original}"\n\n'
                     '💡 Dica: envie um comando como /help para ver opções.'
        }
    
    def _processar_comando(self, comando: str) -> Dict[str, str]:
        """Processa comandos no estilo do bot do Telegram."""
        comando_lower = comando.lower().strip()

        if comando_lower == '/help':
            return {
                'tipo': 'ajuda',
                'texto': (
                    '📋 Comandos disponíveis:\n\n'
                    '/help - Mostra esta ajuda\n'
                    '/listar - Lista motoristas\n'
                    '/placa ABC1234 - Busca por placa\n'
                    '/lh LH_CODIGO - Busca por LH\n'
                    '/addvarios <lote> - Adiciona vários motoristas\n'
                    '/concluido LH/PLACA - Marca como concluído\n'
                    '/cancelado LH/PLACA - Marca como cancelado\n'
                    '/limpar - Limpa todos os motoristas (cuidado!)'
                )
            }

        if comando_lower.startswith('/placa'):
            placa = comando.replace('/placa', '').strip().upper()
            if not placa:
                return {'tipo': 'erro', 'texto': '[ERRO] Uso: /placa ABC1234'}
            return self._buscar_por_valor(placa)

        if comando_lower.startswith('/lh'):
            lh = comando.replace('/lh', '').strip().upper()
            if not lh:
                return {'tipo': 'erro', 'texto': '[ERRO] Uso: /lh 1234567890123'}
            return self._buscar_por_valor(lh)

        if comando_lower.startswith('/listar'):
            return self._listar_motoristas()

        if comando_lower.startswith('/addvarios'):
            bloco = comando.replace('/addvarios', '').strip()
            if not bloco:
                return {
                    'tipo': 'erro',
                    'texto': (
                        "[ERRO] ❌ Nenhum motorista informado.\n\n"
                        "📋 Formato esperado:\n"
                        "LT... NOME PLACA1,PLACA2\n"
                        "Exemplo:\n"
                        "LT0PC301SYPG1 [155030]Jonatan Joao Batista BED4G16,MLF7D60"
                    )
                }
            return self._processar_addvarios(bloco)

        if comando_lower.startswith('/concluido'):
            alvo = comando.replace('/concluido', '').strip().upper()
            if not alvo:
                return {'tipo': 'erro', 'texto': '[ERRO] Uso: /concluido LH_123... ou /concluido ABC1234'}
            return self._marcar_status(alvo, status='concluido')

        if comando_lower.startswith('/cancelado'):
            alvo = comando.replace('/cancelado', '').strip().upper()
            if not alvo:
                return {'tipo': 'erro', 'texto': '[ERRO] Uso: /cancelado LH_123... ou /cancelado ABC1234'}
            return self._marcar_status(alvo, status='cancelado')

        if comando_lower == '/limpar':
            resultado = self.bot.limpar_todos_motoristas()
            return {'tipo': 'limpar', 'texto': f"✅ {resultado.get('mensagem')}"}

        if comando_lower == '/hora':
            agora = datetime.now()
            return {
                'tipo': 'hora',
                'texto': f'🕐 {agora.strftime("%H:%M:%S")}\n📅 {agora.strftime("%d/%m/%Y")}'
            }

        return {
            'tipo': 'erro',
            'texto': f'❌ Comando desconhecido: {comando}\nDigite /help para ver comandos disponíveis.'
        }

    # ===== Integração com lógica do projeto_trabalho =====
    def _buscar_por_valor(self, valor: str) -> Dict[str, str]:
        resultado = self.bot.pesquisar_motoristas(valor)
        if isinstance(resultado, str):
            return {'tipo': 'erro', 'texto': resultado}
        if not resultado:
            return {'tipo': 'erro', 'texto': f'❌ Nenhum motorista encontrado para {valor}'}
        motorista = resultado[0]
        return {
            'tipo': 'sucesso',
            'texto': (
                f"[OK] 🚗 Motorista encontrado:\n"
                f"Nome: {motorista.get('Nome', 'N/A')}\n"
                f"LH: {motorista.get('LH', 'N/A')}\n"
                f"Placas: {motorista.get('Placas', 'N/A')}\n"
                f"Status: {motorista.get('status', 'Ativo')}"
            )
        }

    def _listar_motoristas(self) -> Dict[str, str]:
        lista = self.bot.listar_motoristas()
        if not lista:
            return {'tipo': 'info', 'texto': '⚠️ [AVISO] Nenhum motorista registrado no sistema.'}
        partes: List[str] = [f"📋 [LISTA] Total: {len(lista)} motoristas\n"]
        for idx, m in enumerate(lista, start=1):
            partes.append(
                f"{idx}. 🚗 {m.get('Nome', 'N/A')}\n"
                f"   LH: {m.get('LH', 'N/A')}\n"
                f"   Placas: {m.get('Placas', 'N/A')}\n"
                f"   Status: {m.get('status', 'Ativo')}\n"
            )
        return {'tipo': 'lista', 'texto': "\n".join(partes)}

    def _processar_addvarios(self, bloco: str) -> Dict[str, str]:
        pattern = r'(LT[A-Z0-9]{10,})\s+(?:\[\d+\])?\s*(.+?)\s+([A-Z]{3}\d[A-Z0-9]{3}(?:,[A-Z]{3}\d[A-Z0-9]{3})*)'
        matches = re.findall(pattern, bloco, re.IGNORECASE)
        if not matches:
            return {
                'tipo': 'erro',
                'texto': (
                    "[ERRO] ❌ Nenhum motorista detectado.\n\n"
                    "Formato esperado:\n"
                    "LH [CODIGO]NOME PLACA1,PLACA2\n"
                    "Exemplo:\n"
                    "LT0PC301SYPG1 [155030]Jonatan Joao Batista BED4G16,MLF7D60"
                )
            }

        sucesso = 0
        duplicados = 0
        erros = []
        for idx, (lh, nome, placas) in enumerate(matches, start=1):
            lh = lh.strip().upper()
            nome_limpo = ' '.join(nome.split()).strip()
            placas_fmt = placas.strip().upper()
            if len(lh) < 13:
                erros.append(f"#{idx}: LH muito curto ({lh})")
                continue
            if len(nome_limpo) < 3:
                erros.append(f"#{idx}: Nome inválido ({nome_limpo[:20]})")
                continue
            if len(placas_fmt) < 7:
                erros.append(f"#{idx}: Placas inválidas ({placas_fmt})")
                continue

            retorno = self.bot.adicionar_motoristas(f"{lh} {nome_limpo} {placas_fmt}")
            if retorno['status'] == 'novo':
                sucesso += 1
            elif retorno['status'] == 'duplicado':
                duplicados += 1
            else:
                erros.append(f"#{idx}: {retorno.get('mensagem')}")

        texto_resp = ["📥 Importação concluída!"]
        texto_resp.append(f"✅ Novos: {sucesso}")
        texto_resp.append(f"♻️ Duplicados: {duplicados}")
        if erros:
            texto_resp.append("⚠️ Erros:")
            texto_resp.extend([f"- {e}" for e in erros])
        return {'tipo': 'addvarios', 'texto': "\n".join(texto_resp)}

    def _marcar_status(self, alvo: str, status: str) -> Dict[str, str]:
        # Permite passar placa (7) ou LH (13)
        if len(alvo) == 7:
            res = self.bot.pesquisar_motoristas(alvo)
            if isinstance(res, list) and res:
                alvo = res[0].get('LH', alvo)
        if status == 'concluido':
            retorno = self.bot.marcar_concluido(alvo)
        else:
            retorno = self.bot.marcar_cancelado(alvo)
        if retorno.get('status') == 'sucesso':
            return {'tipo': status, 'texto': f"✅ {retorno.get('mensagem')}"}
        return {'tipo': 'erro', 'texto': f"❌ {retorno.get('mensagem')}"}
    
    def _eh_matematica(self, mensagem: str) -> bool:
        """Verifica se é uma pergunta matemática."""
        return bool(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', mensagem))
    
    def _resolver_matematica(self, mensagem: str) -> Dict[str, str]:
        """Resolve operações matemáticas simples."""
        try:
            # Extrai a expressão matemática
            match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', mensagem)
            if match:
                num1 = float(match.group(1))
                operador = match.group(2)
                num2 = float(match.group(3))
                
                operacoes = {
                    '+': num1 + num2,
                    '-': num1 - num2,
                    '*': num1 * num2,
                    '/': num1 / num2 if num2 != 0 else 'Erro: divisão por zero'
                }
                
                resultado = operacoes.get(operador)
                
                return {
                    'tipo': 'matematica',
                    'texto': f'🔢 {num1} {operador} {num2} = {resultado}'
                }
        except Exception as e:
            pass
        
        return {
            'tipo': 'erro',
            'texto': '❌ Não consegui resolver essa operação.'
        }


# ============================================
# ADICIONE SUAS FUNÇÕES CUSTOMIZADAS AQUI! 🎯
# ============================================

def resposta_personalizada(mensagem: str) -> str:
    """
    Exemplo de função customizada.
    Você pode criar quantas quiser!
    """
    # Sua lógica aqui
    return "Resposta personalizada"
