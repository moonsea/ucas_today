class StaticPagesController < ApplicationController
  def home
    @articles = Article.all;
    @articles = @articles.sort { |x,y| y.comments.length<=>x.comments.length};
    @articles = @articles[0..10];

    @users = Author.all;
    @users = @users.sort{|x,y| y.created_at<=>x.created_at};
    @users = @users[0..4];
  end

  def help
  end
end
