# Copyx API

Esta API permite gerenciar usuários, tweets, comentários, curtidas, seguidores e notificações.

Base URL principal:

```
https://brunops52.pythonanywhere.com/api/
```

# Setup

---

Clone the repository
```http
git clone git@github.com:brunops52/copyx_api.git
```
```http
cd copyx_api/
```

Create the virtual environment
```http
python3 -m venv .venv
```

Activate the virtual environment
```http
source .venv/bin/activate
```

Install dependencies
```http
pip install -r copyx_api/requirements.txt
```

Execute the database migrations.
```http
python copyx_api/manage.py migrate
```

Start the development server.
```http
python copyx_api/manage.py runserver
```


---

## Autenticação

A maioria dos endpoints requer **Bearer Token** no header:

```http
Authorization: Bearer <token>
```

---

## Usuários

### Criar novo usuário

**POST** `/register/`

```json
{
  "username": "notf2",
  "email": "notf2@email.com",
  "password": "senha",
  "first_name": "notf",
  "last_name": "2"
}
```

### Login

**POST** `/login/`

```json
{
  "username_or_email": "notf2",
  "password": "teste"
}
```

### Obter perfil do usuário logado

**GET** `/profile/`

### Atualizar usuário

**PUT** `/profile/`

* Autenticação obrigatória
* Body (form-data):

  * `profile_picture`: arquivo de imagem

### Alterar senha

**PUT** `/change-password/`

```json
{
  "old_password": "senha",
  "new_password": "teste"
}
```

### Detalhes de um usuário

**GET** `/users/{id}/profile/`

---

## Tweets

### Criar tweet

**POST** `/tweets/`

```json
{
  "content": "tweet notf @teste via API! #ebac bbbbb",
  "image": null
}
```

### Listar tweets

**GET** `/tweets/`

### Curtir tweet

**POST** `/tweets/{id}/like/`

### Verificar curtida de um tweet

**GET** `/tweets/{id}/`

### Deletar tweet

**DELETE** `/tweets/{id}/`

---

## Comentários

### Criar comentário

**POST** `/tweets/{id}/comments/`

```json
{
  "content": "Comentário de teste no tweet!"
}
```

### Listar comentários de um tweet

**GET** `/tweets/{id}/comments/`

---

## Bookmarks

### Adicionar tweet aos favoritos

**POST** `/tweets/{id}/bookmark/`

### Listar favoritos

**GET** `/bookmarks/`

---

## Notificações

### Obter notificações

**GET** `/notifications/`

---

## Seguidores e Relacionamentos

### Seguir usuário

**POST** `/users/{id}/follow/`

### Ver se segue um usuário

**GET** `/users/{id}/check-following/`

### Listar seguidores

**GET** `/users/{id}/followers/`

### Listar quem o usuário segue

**GET** `/users/{id}/following/`

### Ver relacionamentos

**GET** `/users/{id}/relationships/`

---

## Timeline e Hashtags

### Ver tweets dos usuários seguidos

**GET** `/timeline`

### Ver tweets por hashtag

**GET** `/hashtags/{hashtag}/`

---

## Pesquisa

### Pesquisa global

**GET** `/search/?q={termo}`

### Pesquisa específica

**GET** `/search/?q={termo}&type=users`

---

## Tokens

### Atualizar token

**POST** `/token/refresh/`

```json
{
  "refresh": "<refresh_token>"
}
```
