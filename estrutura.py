"""
Criar uma classe estruturada para organizar meu codigo
(Copiado de projeto_trabalho/estrutura.py para uso no app_cell)
"""
import time
import json
from datetime import datetime
from pathlib import Path

data = time.localtime()
data_atual =  f'{data.tm_mday}/{data.tm_mon}/{data.tm_year} {data.tm_hour}:{data.tm_min}'

class RoboBolsao:
    def __init__(self, arquivo_dados='motoristas.json'):
        self.arquivo_dados = arquivo_dados
        self.dados_motoristas = {}
        self.historico_status = {}  # Rastreia status: 'ativo', 'concluido', 'cancelado'
        # Carregar dados persistidos
        self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega dados do arquivo JSON se existir."""
        if Path(self.arquivo_dados).exists():
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.dados_motoristas = data.get('motoristas', {})
                    self.historico_status = data.get('historico', {})
            except Exception as e:
                print(f"Aviso ao carregar dados: {e}")
                self.dados_motoristas = {}
                self.historico_status = {}
    
    def _salvar_dados(self):
        """Persiste dados em arquivo JSON."""
        try:
            data = {
                'motoristas': self.dados_motoristas,
                'historico': self.historico_status
            }
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def listar_motoristas(self):
        """Retorna lista de motoristas ativos."""
        return list(self.dados_motoristas.values())
    
    def adicionar_varios_motoristas(self, lista_dados):
        lines = lista_dados.strip().split("\n")
        for line in lines:
            parts = line.split("\t")
            if len(parts) == 3:
                lh = parts[0].strip()
                nome = parts[1].strip()
                placas = [placa.strip() for placa in parts[2].split(",")]
                dado = f"{lh} {nome} {parts[2].strip()}"
                self.adicionar_motoristas(dado)

    def adicionar_motoristas(self, dado):
        """Adiciona motorista com validação de duplicata.
        
        Retorna:
            dict: {'status': 'novo'|'duplicado'|'erro', 'mensagem': str, 'dados': dict|None}
        """
        try:
            dados_tratados = {}
            dados_separados = dado.split()
            dados_tratados['LH'] = dados_separados[0]
            dados_separados.pop(0)
            dados_tratados['Placas'] = dados_separados[-1]
            dados_separados.pop(-1)
            nome = ' '.join(dados_separados)
            dados_tratados['Nome'] = nome
            
            lh = dados_tratados['LH']
            if lh in self.dados_motoristas:
                return {
                    'status': 'duplicado',
                    'mensagem': f'Motorista com LH {lh} já existe no sistema.',
                    'dados': self.dados_motoristas[lh]
                }
            self.dados_motoristas[lh] = dados_tratados
            self._salvar_dados()
            return {
                'status': 'novo',
                'mensagem': f'Motorista {nome} ({lh}) adicionado com sucesso.',
                'dados': dados_tratados
            }
        except IndexError:
            return {
                'status': 'erro',
                'mensagem': 'Formato inválido. Use: /add LH_NUMERO NOME PLACA',
                'dados': None
            }
        except Exception as e:
            return {
                'status': 'erro',
                'mensagem': f'Erro ao tratar dados: {e}',
                'dados': None
            }
   
    def obter_status_motorista(self, lh):
        """Retorna o status atual do motorista."""
        if lh in self.historico_status:
            return self.historico_status[lh]['status']
        elif lh in self.dados_motoristas:
            return 'ativo'
        else:
            return 'não encontrado'

    def pesquisar_motoristas(self, valor_pesquisa):
        resultado = []
        p_user = valor_pesquisa.lower()
        q_caracter = len(p_user)

        if q_caracter == 7:
            for chave, motorista_dict in self.dados_motoristas.items():
                if isinstance(motorista_dict, dict):
                    placa = motorista_dict.get('Placas', '').lower()

                    if len(placa) > 7:
                        placas_lista = [p.strip() for p in placa.split(',')]
                        if p_user in placas_lista:
                            resultado.append(motorista_dict)
                            return resultado
                        
                    if placa == p_user:
                        resultado.append(motorista_dict)
                        return resultado

        elif q_caracter == 13:
            for chave, motorista_dict in self.dados_motoristas.items():
                if isinstance(motorista_dict, dict):
                    lh = motorista_dict.get('LH', '').lower()
                    if lh == p_user:
                        resultado.append(motorista_dict)
                        return resultado
        else:
            text = 'Valor de pesquisa invalido. Insira uma Placa (7 caracteres) ou LH (13 caracteres).'
            return text
    
    def remover_motorista(self, dado_remover):
        """Remove motorista e marca status como cancelado no histórico."""
        try:
            if dado_remover in self.dados_motoristas:
                motorista = self.dados_motoristas.pop(dado_remover)
                self.historico_status[dado_remover] = {
                    'motorista': motorista,
                    'status': 'cancelado',
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'motivo': 'removido'
                }
                self._salvar_dados()
                return {'status': 'sucesso', 'mensagem': f'Motorista {motorista["Nome"]} removido com sucesso.'}
            else:
                return {'status': 'erro', 'mensagem': 'Motorista não encontrado.'}
        except Exception as e:
            return {'status': 'erro', 'mensagem': f'Erro ao remover: {e}'}
    
    def marcar_concluido(self, lh):
        """Marca motorista como concluído."""
        if lh not in self.dados_motoristas:
            return {'status': 'erro', 'mensagem': 'Motorista não encontrado.'}
        
        motorista = self.dados_motoristas[lh]
        self.historico_status[lh] = {
            'motorista': motorista,
            'status': 'concluido',
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'motivo': 'concluído'
        }
        self._salvar_dados()
        return {
            'status': 'sucesso',
            'mensagem': f'Motorista {motorista["Nome"]} marcado como concluído.',
            'dados': motorista
        }
    
    def marcar_cancelado(self, lh):
        """Marca motorista como cancelado."""
        if lh not in self.dados_motoristas:
            return {'status': 'erro', 'mensagem': 'Motorista não encontrado.'}
        
        motorista = self.dados_motoristas[lh]
        self.historico_status[lh] = {
            'motorista': motorista,
            'status': 'cancelado',
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'motivo': 'cancelado'
        }
        self._salvar_dados()
        return {
            'status': 'sucesso',
            'mensagem': f'Motorista {motorista["Nome"]} marcado como cancelado.',
            'dados': motorista
        }
    
    def obter_relatorio_fechamento(self):
        relatorio = []
        for lh, motorista in self.dados_motoristas.items():
            if lh not in self.historico_status:
                relatorio.append({
                    'LH': motorista.get('LH', ''),
                    'Nome': motorista.get('Nome', ''),
                    'Placa': motorista.get('Placas', ''),
                    'Status': 'Ativo',
                    'Data': datetime.now().strftime('%d/%m/%Y %H:%M')
                })
        for lh, historico in self.historico_status.items():
            relatorio.append({
                'LH': lh,
                'Nome': historico['motorista'].get('Nome', ''),
                'Placa': historico['motorista'].get('Placas', ''),
                'Status': 'Concluido' if historico['status'] == 'concluido' else 'Cancelado',
                'Data': historico.get('data', '')
            })
        return relatorio

    def escrever_arquivo(self, nome_arquivo):
        try:
            with open(f'{nome_arquivo}_{data_atual}', 'w') as arquivo:
                for chave, valor in self.dados_motoristas.items():
                    linha = f'LH: {valor["LH"]}, Nome: {valor["Nome"]}, Placas: {valor["Placas"]}\n'
                    arquivo.write(linha)
            print('Dados escritos no arquivo com sucesso!')
        except Exception as e:
            print(f'Erro ao escrever no arquivo: {e}')

    def limpar_todos_motoristas(self):
        try:
            qtd_antes = len(self.dados_motoristas)
            self.dados_motoristas.clear()
            self._salvar_dados()
            return {
                'status': 'sucesso',
                'mensagem': f'Banco de dados limpo com sucesso. {qtd_antes} motoristas removidos.',
                'quantidade_removida': qtd_antes
            }
        except Exception as e:
            return {
                'status': 'erro',
                'mensagem': f'Erro ao limpar banco de dados: {str(e)}',
                'quantidade_removida': 0
            }
