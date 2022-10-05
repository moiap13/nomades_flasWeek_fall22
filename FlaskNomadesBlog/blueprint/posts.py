from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from DB_API import *

from FlaskNomadesBlog import is_logged_in
from FlaskNomadesBlog.forms import FormArticle
from FlaskNomadesBlog.schema import Posts

Myposts = Blueprint('posts', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@Myposts.route('/poster',methods=['POST','GET'])
@is_logged_in
def poster():
    form=FormArticle(request.form)
    if request.method =='POST':
        t=form.titre.data
        c=form.corps.data
        #insertfunctionforarticles
        a = Posts(t,c,session['uid'])
        insertDb(u'posts', None, a.todict())
        flash('Article crée', 'success')
        return redirect(url_for('posts.mesposts'))


    return render_template('posts/poster.html',form=form)

@Myposts.route('/mesposts')
@is_logged_in
def mesposts():
        posts=getDocumentsWhere(u'posts', u'uid', u'==', session['uid'])
        return render_template('posts/mesposts.html',posts=posts)

@Myposts.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    deleteDB(u'posts', id)
    flash('Article Deleted', 'success')

    return redirect(url_for('posts.mesposts'))

@Myposts.route('/post/<string:id>/')
def article(id):
    post=getDocumentDB(u'posts',id)
    return render_template('posts/post.html',post=post)