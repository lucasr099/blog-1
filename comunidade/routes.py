
from flask import Flask, render_template, request, redirect, url_for, flash
from comunidade import app
from comunidade.forms import formLogin, formCriarConta, formEditarConta, formCriarPost
from comunidade.models import Usuario, database, Post
from comunidade import Bcrypt, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from werkzeug.exceptions import abort






@app.route("/")
def home():
   posts = Post.query.order_by(Post.id.desc())
   usuario = current_user
   return render_template('home.html', posts=posts, usuario=usuario)

@app.route("/contato")
def contato():
        return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
        lista_usuarios = Usuario.query.all()
        return render_template('usuarios.html', 
    lista_usuarios=lista_usuarios)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_Login = formLogin()
    form_CriarConta = formCriarConta()
    if form_Login.validate_on_submit() and 'submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_Login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_Login.senha.data):
            login_user(usuario, remember=form_Login.lembrar_dados)
            flash(f'Login efetuado com sucesso: {form_Login.email.data}', 'success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                 return redirect(url_for('home'))
            
            return redirect(url_for('home'))
        else:
             flash(f'Falha no Login, Senha ou E-mail incorreto', 'danger')
    if form_CriarConta.validate_on_submit() and 'submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_CriarConta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_CriarConta.username.data, email=form_CriarConta.email.data, senha= senha_cript )
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso: {form_CriarConta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_Login=form_Login, form_CriarConta=form_CriarConta)

@app.route('/sair')
def sair():
    logout_user()
    flash('Logout efetuado com sucesso','success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'foto_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = formCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso: {form.titulo.data}', 'success')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form=form)

def salvar_imagem(imagem): 
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path,'static/foto_perfil', nome_arquivo)
    tamanho_imagem = (150, 150)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho_imagem)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo
     



@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = formEditarConta()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.time_futebol = form.time_futebol.data
        
        # Salvar a imagem do perfil, se fornecida...
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
            
        database.session.commit()
        flash('Perfil editado com sucesso','success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.time_futebol.data = current_user.time_futebol
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def exibir_post(id):
    post = Post.query.get_or_404(id)
    usuario = current_user
    if current_user == post.autor:
        form = formCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash(f'Post editado com sucesso: {form.titulo.data}', 'success')
            return redirect(url_for('home', id=post.id))
    else:
        form = None
    return render_template('post.html', post=post, usuario=usuario, form=form)

@app.route('/post/<int:id>/deletar', methods=['GET', 'POST'])
@login_required
def excluir_post(id):
    post = Post.query.get_or_404(id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash(f'Post deletado com sucesso: {post.titulo}', 'success')
        return redirect(url_for('home'))
    else:
        abort(403)