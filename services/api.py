import requests
import bcrypt
import os

BASE_URL = "https://dszzjdzferfxnbfthdmi.supabase.co/rest/v1"
API_KEY = "sb_publishable_rEJ5evi0QT8-caj7ezGkmw_nZ9EUmvS"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def login(email, senha):
    try:
        r = requests.get(
            f"{BASE_URL}/usuarios",
            headers=HEADERS,
            params={
                "email": f"eq.{email}",
                "admin": "eq.true"
            },
            timeout=10
        )
        if r.status_code == 200:
            usuario = r.json()
            
            if len(usuario) == 0:
                return {"status": "erro", "msg": "Usuário não encontrado"}
            
            usuario = usuario[0]
            
            senha_hash = usuario.get("senha").encode('utf-8')
            senha = senha.encode('utf-8')
            
            if bcrypt.checkpw(senha, senha_hash):
                return {
                    "status": "sucesso", 
                    "usuario": {
                        "id": usuario["id"],
                        "nome": usuario["nome"]
                    }
                }
                
            else:
                return {"status": "erro", "msg": "Senha incorreta"}
        else:
            return {
                "status": "erro",
                "msg": f"Erro HTTP {r.status_code}"
            }
                
    except Exception as e:
        return {"status": "erro", "msg": str(e)}


def get_eventos(usuario_id):
    try:
        r = requests.get(
            f"{BASE_URL}/eventos?usuario_id=eq.{usuario_id}",
            headers=HEADERS,
            timeout=10
        )
        return r.json()
    
    except Exception as e:
        print(e)
        return []


def validar_qr(codigo, evento_id):
    try:
        # O filtro "select=id, usado, usuario_id" é para otimizar a consulta, 
        # trazendo apenas os campos necessários
        url = (
            f"{BASE_URL}/ingressos"
            f"?codigo=eq.{codigo}"
            f"&evento_id=eq.{evento_id}"
            f"&select=id,usado,usuario_id"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        
        print(f"DEBUG Validar: {url}")
        print(f"DEBUG Status: {response.status_code}")

        if response.status_code != 200:
            return {"status": "erro", "msg": f"Erro API: {response.status_code}"}

        dados = response.json()
        print(f"DEBUG Dados: {dados}")

        # Não encontrado
        if not dados:
            return {
                "status": "erro",
                "msg": "Ingresso inválido ou token expirado"
            }
        ingresso = dados[0]
        
        # Já usado (== True)
        if ingresso["usado"]:
            return {
                "status": "erro",
                "msg": "Ingresso já utilizado"
            }

        # Busca o nome do banco para exibir na mensagem de sucesso
        usuario_url = (
            f"{BASE_URL}/usuarios"
            f"?id=eq.{ingresso['usuario_id']}"
            f"&select=nome"
        )
        usuario_response = requests.get(
            usuario_url,
            headers=HEADERS,
            timeout=10
        )

        usuario = usuario_response.json()[0]

        # Marcando como usado
        update_url = (
            f"{BASE_URL}/ingressos?id=eq.{ingresso['id']}"
        )

        patch_response = requests.patch(
            update_url,
            headers=HEADERS,
            json={
                "usado": True
            },
            timeout=10
        )
        
        if patch_response.status_code not in [200, 204]:
            return {
                "status": "erro",
                "msg": "Erro ao validar ingresso"
            }

        # -----------------------------------
        # CONTAR TOTAL DE ENTRADAS
        # -----------------------------------
        count_url = (
            f"{BASE_URL}/ingressos"
            f"?evento_id=eq.{evento_id}"
            f"&usado=eq.true"
            f"&select=id")
        # Retorna o total de registros
        count_headers = {
            **HEADERS,
            "Prefer": "count=exact"
        }
        
        response = requests.get(
            count_url,
            headers=count_headers,
            timeout=10
        )

        total = int(response.headers["Content-Range"].split("/")[-1])

        # SUCESSO
        return {
            "status": "ok",
            "nome": usuario["nome"],
            "total": total
        }

    except Exception as e:
        return {"status": "erro", "msg": str(e)}