# <img src = './front/src/assets/logo.png' width=40 height=40 > 개취무비

## 📚 목차

- [ 개취무비](#-개취무비)
  - [📚 목차](#-목차)
  - [🗓️프로젝트 개요](#️프로젝트-개요)
    - [진행 기간](#진행-기간)
    - [기술 스택](#기술-스택)
  - [👯‍♀️팀원 정보 및 업무 분담 내역](#️팀원-정보-및-업무-분담-내역)
  - [📢서비스 소개](#서비스-소개)
    - [서비스 기획 목표](#서비스-기획-목표)
    - [ERD](#erd)
    - [Wireframe](#wireframe)
      - [Figma](#figma)
    - [영화 추천 알고리즘](#영화-추천-알고리즘)
    - [gpt - 영화 추천 알고리즘](#gpt---영화-추천-알고리즘)
  - [💻기능 구현/ 요구사항](#기능-구현-요구사항)
    - [홈 화면](#홈-화면)
    - [영화 검색 페이지](#영화-검색-페이지)
    - [영화 디테일 페이지](#영화-디테일-페이지)
    - [배우 디테일 페이지](#배우-디테일-페이지)
    - [리뷰 생성](#리뷰-생성)
    - [리뷰 페이지](#리뷰-페이지)
    - [랜덤 추천](#랜덤-추천)
    - [영화 추천](#영화-추천)
    - [챗봇](#챗봇)
    - [signup/login](#signuplogin)
    - [프로필](#프로필)
    - [🎯 요구 사항](#-요구-사항)
  - [👍 느낀 점](#-느낀-점)
  - [📁 오픈소스 출처](#-오픈소스-출처)
   



## 🗓️프로젝트 개요

### 진행 기간
2023.05.16 ~ 2022.05.24 오전 9시 (9일간)

### 기술 스택

![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-330F63?style=for-the-badge&logo=notion&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=1D9FD7)![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
  
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

## 👯‍♀️팀원 정보 및 업무 분담 내역

고충원 - 화면 설계서 제작 및 컴포넌트 설계, OST, 영화 명대사 데이터 수집 및 정제, Front-END 개발 및 UI, UX 개선

임성훈 - 영화 데이터 수집 및 정제, 추천 알고리즘 개발, ERD 설계, DB 구출 및 Back-End 개발

## 📢서비스 소개

### 서비스 기획 목표

사용자가 좋아하는 영화와 싫어하는 영화 정보를 자세히 알려주면 사용자가 싫어하는 영화의 키워드는 최대한 피하고 좋아하는 영화 위주로 영화를 추천함으로써 영화를 추천받아서 영화를 보게 되었을때 시청하게 되는 영화가 취향에 맞지 않아 시간을 날리게 되는 상황을 피할수 있도록 만들어 준다.<br>
그래서 사용자는 쉽게 자신의 취향에 맞는 영화를 찾아 시청할수 있는 서비스를 만드는 것이 기획 목표이다.

### ERD

![Alt text](assets/image.png)


### Wireframe

#### Figma
![Alt text](assets/mockup.PNG)



### 영화 추천 알고리즘

영화마다 가지고 있는 키워드들이 있고 그 키워드 모델과 유저 모델을 관계 맺어, count필드가 들어 있는 Userkeyword모델을 생성합니다.

그 후 좋아요 누른 영화의 키워드마다 +1,
싫어요 누른 영화의 키워드마다 -1을 합니다.

```
# 좋아요 누르기
@api_view(['POST'])
def like_movie(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 좋아요가 눌러져 있을 때
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        # 키워드-1
        remove_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    # 좋아요 안 눌러져 있을 때
    else:
        if movie.dislike_users.filter(pk=user.pk).exists():
            movie.dislike_users.remove(user)
            # 싫어요 취소 되니까 키워드+1
            add_user_keywords(user, movie)
        movie.like_users.add(user)
        # 키워드 +1
        add_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
```
 - 싫어요 누르는 함수도 위와 똑같으니 생략

```
# 키워드 + 1
def add_user_keywords(user, movie):
    # id를 받기 위해 values_list 사용
    keyword_ids = movie.keywords.values_list('id', flat=True)
    for keyword_id in keyword_ids:
        # 필드에 키워드가 없으면 생성
        user_keyword, created = UserKeyword.objects.get_or_create(user=user, keyword_id=keyword_id)
        # 카운트
        user_keyword.count += 1
        user_keyword.save()
    return
```
- 키워드 -1 함수도 위와 똑같으니 생략

count가 0보다 큰 키워드들만 추출해서 단순히 좋아하는 keyword의 개수가 아닌 내가 좋아요 누른 count의 합을 기준으로 데이터를 뽑아왔습니다.
```
# 영화 추천 알고리즘
@api_view(['GET'])
def recommended(request, user_pk, page_pk):
    # count가 0보다 큰 keywords를 추출
    user_keywords = UserKeyword.objects.filter(user_id=user_pk, count__gt=0)
    
    # keywords id 리스트 생성
    keyword_ids = user_keywords.values_list('keyword_id', flat=True)

    # 사용자가 좋아요한 영화 제외하고, 각 키워드의 count 합을 기준으로 큰 순서부터 정렬
    recommended_movies = Movie.objects.filter(
        keywords__in=keyword_ids
    ).exclude(
        like_users__id=user_pk
    ).annotate(
        keyword_match_count=Sum(
            Case(
                *[
                    When(keywords=keyword_id, then=user_keyword.count) 
                    for keyword_id, user_keyword in zip(keyword_ids, user_keywords)
                ],
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-keyword_match_count').distinct()
    
    # 한 페이지당 10개의 데이터 저장
    paginator = Paginator(recommended_movies, 10)
    
    page = request.GET.get('page', page_pk)
    page_movies = paginator.get_page(page)
    serializer = MovieSerializer(page_movies, many=True)
    
    return Response(serializer.data)
```
### gpt - 영화 추천 알고리즘
1. 사용자가 좋아요 한 영화 리스트를 db에 요청을 보내 가져옵니다.
```js
const chatmovielist = ref([])
const getlikeMovie = async () => {
    try {
const response = await axios.get(`http://127.0.0.1:8000/movies/${localStorage.getItem('userid')}/user_like_movie`);

response.data.like_movies.forEach(element => {
    chatmovielist.value.push(element.title);
});
console.log(chatmovielist.value);
} catch (error) {
console.error(error);
}
};
```
2. db에 요청을 보내 가져온 데이터를 리스트 형태로 담아 챗 gpt api에 요청을 보냅니다.
```js
const chatrecommend = async function () {
  const api = 'https://api.openai.com/v1/chat/completions';
  const key = '';

  try {
    const res = await axios.post(api, {
      model: 'gpt-4o',
      messages: [{
        role: 'user',
        content: `${chatmovielist.value}를 기반으로 영화를 추천해 주는데 ${chatmovielist.value} 영화는 빼고 추천해줘 
        ''사이의 문자를 tmbd movie id로 바꿔서 10개만 담에서 []만 보내줘 ${chatmovielist.value}영화가 너가 보내주는 리스트에 들어있다면 다 빼줘`
      }],
    }, {
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }
    });
    chatrecommendlist.value = res.data.choices[0].message.content.match(/\d+/g).map(Number);
    console.log(chatrecommendlist.value);
  } catch (err) {
    chatlog.value.push({ my: inputchat.value, gpt: '고장' });
    console.error(err);
  }
  inputchat.value = '';
};
```
3. 가져온 tmdb  movie id 를 tmdb api로 요청을 보냅니다.
```js

const gptMovie = async () => {
  for (const movieid of chatrecommendlist.value) {
    console.log(movieid);
    const options = {
      method: 'GET',
      url: `https://api.themoviedb.org/3/movie/${movieid}?api_key=${myid}`,
      params: { language: 'ko-KR' },
      headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMjZlYzkyNTYwMmI2NTlmNjIzY2NmYjlhNDYzOTZlMyIsInN1YiI6IjY2M2Q3ZDZjOTE0ZDU3Mzk3OGE0MTcwNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FLkVpZ5-Oy3sFrFpCVurtGQ4vJ-WxnmJhBAzSp7VK-M'
      }
    };
    try {
      const response = await axios.request(options);
      gptlist.value.push(response.data);
    } catch (error) {
      console.error(error);
    }
  }
};
```
4. tmdb에서 받은 정보를 페이지에 렌더링 합니다.

## 💻기능 구현/ 요구사항

### 홈 화면
![image](assets/main.PNG)


### 영화 검색 페이지
![image](assets/index.png)
### 영화 디테일 페이지
![image](assets/moviedetail.png)
### 배우 디테일 페이지
![image](assets/actor.png)
### 리뷰 생성 
![image](assets/createreview.png)
### 리뷰 페이지
![image](assets/review.png)

### 랜덤 추천
![image](assets/random.png)
###  영화 추천
![image](assets/movierecommend.png)
### 챗봇
![image](assets/chatbot.png)

### signup/login
![image](assets/signup.png)
![image](assets/login.png)

### 프로필
![image](assets/profile.png)


### 🎯 요구 사항
- 구현성공 ⭕
- 구현실패 ❌
- 필수 요구사항 ✅
- 추가로 구현 한 기능 💖


1. 영화 데이터 ⭕ ✅
2. 영화 추천 알고리즘 ⭕ ✅
3. API ⭕ ✅
4. 커뮤니티 ⭕ ✅
5. README ⭕ ✅
6. Ai Chat bot 기능 ⭕💖
7. Ai 기반 Chat GPT 가 해주는 영화 추천 ⭕💖
8. 영화 검색 알고리즘 ⭕💖
9. 랜덤 영화 추천 알고리즘 ⭕💖

## 👍 느낀 점

임성훈 <br>
처음에 했던 걱정과 달리 좋은 결과물이 나온 것 같아 뿌듯합니다.<br>
시작은 힘들었지만 직접 코드를 짜며 기능이 구현될 때마다 재미가 생기고 점점 욕심도 늘었습니다. 그러다 보니 구현하고 싶은 기능들이 많이 있었지만 시간이 부족해 원하는 기능을 모두 넣을 수는 없었습니다. 그래도 이 프로젝트를 통해 많이 성장한 것을 느꼈고 추후에는 더 잘할 수 있을 것이라는 자신감이 생겼습니다.<br>
충원이형이 너무 잘해주셔서 좋은 결과가 나왔고 재밌게 프로젝트를 진행할 수 있었습니다. 감사합니다!!

고충원 <br>
처음에 프로젝트를 시작했을때에는 어떻게 꾸려나가야 할지 막막하고 앞으로의 일들이 걱정이 됐었습니다.<br>
그래서 처음에 아이디어를 짜고 구현할 계획을 할때에 최소한으로 기능을 구현하자고 얘기했었지만 성훈이랑 힘을 합쳐 하나하나 해결해 나가다 보니 할만하다고 느끼게 되었습니다.<br>
그래서 욕심을 조금 내서 이런 기능도 넣고 저런 기능도 넣게 되었습니다.<br>
첫 프로젝트라서 헤메기도 했고 어려웠지만 보람차게 프로젝트를 진행할수 있었고 마음 맞는 좋은 팀원과 함께 프로젝트를 진행해서 즐겁게 했습니다 .!!

## 📁 오픈소스 출처

- TMDB : https://developer.themoviedb.org/reference/intro/getting-started 
- GPT : https://openai.com/index/openai-api/