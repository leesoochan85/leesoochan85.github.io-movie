document.addEventListener('DOMContentLoaded', function () {
  fetch('/api/posts/')
    .then(response => {
      if (!response.ok) throw new Error('게시글 데이터를 불러올 수 없습니다.');
      return response.json();
    })
    .then(posts => {
      const postGrid = document.getElementById('postGrid');
      postGrid.innerHTML = ''; 

      posts.slice(0, 6).forEach((post) => {
        const card = document.createElement('div');
        card.className = 'post-card';
        const imageUrl = post.image || '/static/images/noimage.jpg';  //이미지 없을 경우 기본값
        card.innerHTML = `
          <img src="${imageUrl}" alt="" class="post-image" />
          <div class="post-info">
            <h3>${post.title}</h3>
            <p>${post.content || ''}</p>
            <div class="post-meta">
              <span><i class="fas fa-user"></i> ${post.writer}</span>
              <span><i class="fas fa-calendar-alt"></i> ${post.date}</span>
            </div>
          </div>
        `;

        card.addEventListener('click', () => {
          window.location.href = `/post/${post.id}/`;
        });

        postGrid.appendChild(card);
      });

      if (posts.length === 0) {
        postGrid.innerHTML = '<p>게시글이 없습니다.</p>';
      }
    })
    .catch(error => {
      console.error('게시글 불러오기 오류:', error);
      const postGrid = document.getElementById('postGrid');
      postGrid.innerHTML = '<p style="color:red;">게시글을 불러오는 데 실패했습니다.</p>';
    });

  // 추천 영화 데이터 (더미)
  const movies = [
    { id: 101, title: '영화 제목 더미1', director: '크리스토퍼 놀란', rating: 9.5, genre: '스릴러' },
    { id: 102, title: '영화 제목 더미2', director: '데이미언 셔젤', rating: 9.0, genre: '드라마' },
    { id: 103, title: '영화 제목 더미3', director: '최동훈', rating: 8.9, genre: '액션' },
    { id: 104, title: '영화 제목 더미4', director: '존 카니', rating: 8.8, genre: '코미디' },
  ];

  const movieList = document.getElementById('movieList');
  movies.sort((a, b) => b.rating - a.rating).forEach((movie) => {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.innerHTML = `
      <div class="movie-info">
        <strong>${movie.title}</strong>
        <span><i class="fas fa-user-tie"></i> ${movie.director} · ${movie.genre}</span>
      </div>
      <div class="movie-rating">⭐ ${movie.rating.toFixed(1)}</div>
    `;

    card.addEventListener('click', () => {
      window.location.href = `/movie/${movie.id}`;
    });

    movieList.appendChild(card);
  });

  // 슬라이더 코드
  const slider = document.getElementById('slider');
  const images = slider.querySelectorAll('img');
  const prevBtn = document.querySelector('.slide-btn.prev');
  const nextBtn = document.querySelector('.slide-btn.next');
  const indicatorsContainer = document.getElementById('sliderIndicators');
  let currentIndex = 0;
  let autoSlideInterval;

  images.forEach((_, index) => {
    const indicator = document.createElement('div');
    indicator.className = `indicator ${index === 0 ? 'active' : ''}`;
    indicator.addEventListener('click', () => {
      currentIndex = index;
      updateSlide();
      resetAutoSlide();
    });
    indicatorsContainer.appendChild(indicator);
  });

  function updateSlide() {
    const offset = -currentIndex * 100;
    slider.style.transform = `translateX(${offset}%)`;

    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
      indicator.classList.toggle('active', index === currentIndex);
    });
  }

  function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
  }

  function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % images.length;
      updateSlide();
    }, 4000);
  }

  prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateSlide();
    resetAutoSlide();
  });

  nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % images.length;
    updateSlide();
    resetAutoSlide();
  });

  startAutoSlide();

  const sliderContainer = document.querySelector('.slider-container');
  sliderContainer.addEventListener('mouseenter', () => {
    clearInterval(autoSlideInterval);
  });

  sliderContainer.addEventListener('mouseleave', () => {
    startAutoSlide();
  });


});
