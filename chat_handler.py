"""
Sistema de processamento de mensagens customizável.
Adicione suas próprias regras de resposta aqui.
"""

import re
from typing import Dict, Optional
from datetime import datetime


class ChatHandler:
    """Gerenciador de lógica de respostas."""
    
    def __init__(self):
        self.conversa_historico = {}
        
    def processar_mensagem(self, user_id: str, mensagem: str) -> Dict[str, str]:
        """
        Processa mensagem e retorna resposta.
        
        Args:
            user_id: ID do usuário
            mensagem: Mensagem recebida
            
        Returns:
            Dict com tipo de resposta e texto
        """
        mensagem = mensagem.strip().lower()
        
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
        
        # Comandos básicos
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
        
        # Perguntas sobre o sistema
        if 'como funciona' in mensagem or 'o que você faz' in mensagem:
            return {
                'tipo': 'info',
                'texto': 'Sou um assistente virtual customizável! 🤖\n\n'
                         'Você pode me programar para responder qualquer coisa. '
                         'Edite o arquivo chat_handler.py para adicionar suas próprias regras!'
            }
        
        # Comandos com /
        if mensagem.startswith('/'):
            return self._processar_comando(mensagem)
        
        # Perguntas matemáticas simples
        if self._eh_matematica(mensagem):
            return self._resolver_matematica(mensagem)
        
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
            'texto': f'Recebi sua mensagem: "{mensagem}"\n\n'
                     '💡 Dica: Você pode programar respostas customizadas '
                     'editando o arquivo chat_handler.py!'
        }
    
    def _processar_comando(self, comando: str) -> Dict[str, str]:
        """Processa comandos que começam com /"""
        
        if comando == '/help':
            return {
                'tipo': 'ajuda',
                'texto': '📋 Comandos disponíveis:\n\n'
                         '/help - Mostra esta ajuda\n'
                         '/hora - Mostra hora atual\n'
                         '/historico - Mostra suas últimas mensagens\n'
                         '/limpar - Limpa histórico\n\n'
                         '💡 Adicione seus próprios comandos no chat_handler.py!'
            }
        
        elif comando == '/hora':
            agora = datetime.now()
            return {
                'tipo': 'hora',
                'texto': f'🕐 {agora.strftime("%H:%M:%S")}\n'
                         f'📅 {agora.strftime("%d/%m/%Y")}'
            }
        
        elif comando.startswith('/historico'):
            # Implementar lógica de histórico
            return {
                'tipo': 'historico',
                'texto': '📜 Histórico de conversas (em desenvolvimento)'
            }
        
        elif comando == '/limpar':
            return {
                'tipo': 'limpar',
                'texto': '✅ Histórico limpo!'
            }
        
        else:
            return {
                'tipo': 'erro',
                'texto': f'❌ Comando desconhecido: {comando}\n'
                         'Digite /help para ver comandos disponíveis.'
            }
    
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
