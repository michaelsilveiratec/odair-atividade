# main.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
import pandas as pd

app = FastAPI(
    title="API de Dados de Vendas",
    description="API para gerenciar produtos e vendas",
    version="1.0.0"
)

# Dados simulados
vendas_df = pd.DataFrame({
    'id': range(1, 11),
    'produto': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Headphone',
                'Webcam', 'SSD', 'RAM', 'GPU', 'CPU'],
    'categoria': ['Computadores', 'Acessórios', 'Acessórios', 'Periféricos', 'Áudio',
                  'Periféricos', 'Componentes', 'Componentes', 'Componentes', 'Componentes'],
    'preco': [3500, 150, 200, 1200, 350, 180, 450, 300, 2000, 1500],
    'quantidade_vendida': [12, 85, 63, 35, 42, 30, 55, 70, 22, 25]
})

# Pydantic Models
class Produto(BaseModel):
    id: int
    produto: str
    categoria: str
    preco: float
    quantidade_vendida: int

class ProdutoCreate(BaseModel):
    produto: str
    categoria: str
    preco: float
    quantidade_vendida: int

    @validator("preco", "quantidade_vendida")
    def nao_negativo(cls, v):
        if v < 0:
            raise ValueError("Deve ser maior ou igual a zero")
        return v

# Root
@app.get("/")
def read_root():
    return {"mensagem": "API de Dados de Vendas"}

# Listagem com filtros e paginação
@app.get("/produtos", response_model=List[Produto])
def get_produtos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria", example="Acessórios"),
    min_preco: Optional[float] = Query(None, description="Preço mínimo", example=100),
    max_preco: Optional[float] = Query(None, description="Preço máximo", example=2000),
    skip: int = Query(0, description="Número de itens a pular"),
    limit: int = Query(10, description="Número máximo de itens retornados")
):
    df = vendas_df.copy()
    
    if categoria:
        df = df[df['categoria'] == categoria]
    if min_preco is not None:
        df = df[df['preco'] >= min_preco]
    if max_preco is not None:
        df = df[df['preco'] <= max_preco]
    
    df_pag = df.iloc[skip : skip + limit]
    return df_pag.to_dict(orient='records')

# Detalhe de produto por ID
@app.get("/produtos/{produto_id}", response_model=Produto)
def get_produto(produto_id: int):
    produto = vendas_df[vendas_df['id'] == produto_id]
    if produto.empty:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto.iloc[0].to_dict()

# Criar novo produto
@app.post("/produtos", response_model=Produto)
def create_produto(produto: ProdutoCreate):
    global vendas_df
    novo_id = vendas_df['id'].max() + 1 if not vendas_df.empty else 1
    novo_produto = {
        'id': novo_id,
        **produto.dict()
    }
    vendas_df = pd.concat([vendas_df, pd.DataFrame([novo_produto])], ignore_index=True)
    return novo_produto

# Atualizar produto (opcional)
@app.put("/produtos/{produto_id}", response_model=Produto)
def update_produto(produto_id: int, produto: ProdutoCreate):
    global vendas_df
    idx = vendas_df.index[vendas_df['id'] == produto_id].tolist()
    if not idx:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    vendas_df.loc[idx[0], ['produto', 'categoria', 'preco', 'quantidade_vendida']] = \
        produto.produto, produto.categoria, produto.preco, produto.quantidade_vendida
    return vendas_df.loc[idx[0]].to_dict()

# Deletar produto
@app.delete("/produtos/{produto_id}")
def delete_produto(produto_id: int):
    global vendas_df
    idx = vendas_df.index[vendas_df['id'] == produto_id].tolist()
    if not idx:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    vendas_df = vendas_df.drop(idx[0]).reset_index(drop=True)
    return {"mensagem": "Produto removido com sucesso"}
