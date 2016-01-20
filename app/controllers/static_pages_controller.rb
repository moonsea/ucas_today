class StaticPagesController < ApplicationController
  def home
    @articles = Article.all;
    @articles.sort { |x,y| y.comments.length<=>x.comments.length};
    @articles.limit(10);
    @users = Author.all;
    @users.sort{|x,y| y.created_at<=>x.created_at};
    @users.limit(6);
  end

  def help
  end
end
