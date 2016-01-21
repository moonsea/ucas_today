class CommentsController < ApplicationController  
  def create  
    params.permit!
    if session[:author_id] != nil
      @article = Article.find(params[:article_id])  
      @comment = @article.comments.build(params[:comment])  
      @comment.author_id=session[:author_id]
      @comment.save
    end
  
    redirect_to @article
  end  
  
  def destroy 
    params.permit! 
    @comment = Comment.find(params[:id])  
    @comment.destroy  

   redirect_to @comment.article
  end  
end  

