class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]

  # GET /articles
  # GET /articles.json

  def index
    @articles = Article.all
  end
  def search_news
    @articles = Article.where("info like ? or title like ?","%"+params[:keywords]+"%","%"+params[:keywords]+"%")
    @users = Author.all;
    @users = @users.sort{|x,y| y.created_at<=>x.created_at};
    @users = @users[0..4];
  end
  def recommend
    @author = Author.find(session[:author_id])
    @articles = Article.where(info:@author.info)
  end
  def info
    @articles = Article.where(info:params[:info])
    @users = Author.all;
    @users = @users.sort{|x,y| y.created_at<=>x.created_at};
    @users = @users[0..4];
    render 'all'
  end
  def all
    @articles = Article.all
  end
  # GET /articles/1
  # GET /articles/1.json
  def show
  end

  # GET /articles/new
  def new
    @article = Article.new	
  end

  # GET /articles/1/edit
  def edit
  end

  # POST /articles
  # POST /articles.json
  def create
    @article = Article.new(article_params)
    if logged_in?
	@article.author_id=session[:author_id]
    else 
	@article.author_id=1
    end
    respond_to do |format|
      if @article.save
        format.html { redirect_to @article, notice: '文章创建成功.' }
        format.json { render :show, status: :created, location: @article }
      else
        format.html { render :new }
        format.json { render json: @article.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /articles/1
  # PATCH/PUT /articles/1.json
  def update
    respond_to do |format|
      if @article.update(article_params)
        format.html { redirect_to @article }
        format.json { render :show, status: :ok, location: @article }
      else
        format.html { render :edit }
        format.json { render json: @article.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /articles/1
  # DELETE /articles/1.json
  def destroy
    @article.destroy
    respond_to do |format|
      format.html { redirect_to current_author }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_article
      @article = Article.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def article_params
      params.require(:article).permit(:title, :text, :author_id,:info)
    end
end
