document.addEventListener('DOMContentLoaded', function () {
    // 최신 게시글 6개 더미테이터 및 실제 작동 코드입니다.
    const posts = [
      { id: 1, title: '글 제목 더미 데이터 01', content: '게시글의 내용 데이터가 삽입될 자리입니다.', image: '/static/images/movie01.jpg' },
      { id: 2, title: '글 제목 더미 데이터 02', content: '내용02', image: '/static/images/movie02.jpg' },
      { id: 3, title: '글 제목 더미 데이터 03', content: '내용03', image: '/static/images/movie03.jpg' },
      { id: 4, title: '글 제목 더미 데이터 04', content: '내용04', image: '/static/images/movie04.jpg' },
      { id: 5, title: '글 제목 더미 데이터 05', content: '내용05', image: '/static/images/movie05.jpg' },
      { id: 6, title: '글 제목 더미 데이터 06', content: '내용06', image: '/static/images/movie06.jpg' },
    ];
  
    const postGrid = document.getElementById('postGrid');
    posts.forEach((post, index) => {
      const card = document.createElement('div');
      card.className = `post-card ${index % 2 === 0 ? 'large' : 'small'}`;
      card.innerHTML = `
        <img src="${post.image}" alt="${post.title}" class="post-image" />
        <div class="post-info">
          <h3>${post.title}</h3>
          <p>${post.content}</p>
        </div>
      `;
      postGrid.appendChild(card);
    });
  
    // 추천 영화 부분 더미데이터 및 실제 작동 코드입니다.
    const movies = [
      { id: 101, title: '영화 제목 더미1', director: '크리스토퍼 놀란', rating: 9.5 },
      { id: 102, title: '영화 제목 더미2', director: '데이미언 셔젤', rating: 9.0 },
      { id: 103, title: '영화 제목 더미3', director: '최동훈', rating: 8.9 },
      { id: 104, title: '영화 제목 더미4', director: '존 카니', rating: 8.8 },
    ];
  
    const movieList = document.getElementById('movieList');
    movies.sort((a, b) => b.rating - a.rating).forEach((movie) => {
      const card = document.createElement('div');
      card.className = 'movie-card';
      card.innerHTML = `
        <div class="movie-info">
          <strong>${movie.title}</strong><br/>
          <span>🎬 ${movie.director}</span>
        </div>
        <div class="movie-rating">⭐ ${movie.rating.toFixed(1)}</div>
      `;
      movieList.appendChild(card);
    });
  
    // 단순 슬라이더 구현 코드입니다.
    const slider = document.getElementById('slider');
    const images = slider.querySelectorAll('img');
    const prevBtn = document.querySelector('.slide-btn.prev');
    const nextBtn = document.querySelector('.slide-btn.next');
  
    let currentIndex = 0;

    let autoSlideInterval = setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        updateSlide();
      }, 4000);
  
    function updateSlide() {
      const offset = -currentIndex * 100;
      slider.style.transform = `translateX(${offset}%)`;
    }
  
    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      updateSlide();
    });
  
    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % images.length;
      updateSlide();
    });
  });
  
  
  