document.addEventListener('DOMContentLoaded', function () {
    const movies = [];

    for (let i = 1; i <= 10; i++) { //더미데이터 생성용 코드입니다.
      movies.push({
        id: i,
        title: `영화 더미데이터${i}`,
        overview: `내용 더미${i} - 더미데이터 ${i}번째 `,
        release_date: `2024-04-${(i % 30 + 1).toString().padStart(2, '0')}`,
        vote_average: i % 11,
        genres: ['액션', '드라마', 'SF', '로맨스', '애니메이션'][i % 5] + ',' + ['판타지', '스릴러', '코미디', '가족', '뮤지컬'][i % 5],
      });
    }
    
  
    const PER_PAGE = 8;
    let currentPage = 1;
    let selectedGenres = [];
  
    const movieGrid = document.getElementById('movieGrid');
    const pagination = document.getElementById('pagination');
    const genreForm = document.getElementById('genreForm');
  
    //더미 데이터입니다. 실제 연동할 때 지워주세요.
    const allGenres = Array.from(new Set(
      movies.flatMap(m => m.genres.split(',').map(g => g.trim())) //장르의 경우, 현재 데이터베이스 내 모든 영화의 genres 필드를 꺼내 배열 형태로 추출합니다. [,로 구분합니다.]
    ));
  
    // 장르 필터 체크박스 렌더링
    function renderGenreCheckboxes() {
      genreForm.innerHTML = '';
      allGenres.forEach(genre => {
        const id = `genre-${genre.replace(/\s+/g, '-')}`;
        genreForm.innerHTML += `
          <label>
            <input type="checkbox" value="${genre}" id="${id}">
            ${genre}
          </label>
        `;
      });
  
      genreForm.querySelectorAll('input[type="checkbox"]').forEach(input => {
        input.addEventListener('change', () => {
          selectedGenres = Array.from(genreForm.querySelectorAll('input:checked')).map(cb => cb.value);
          currentPage = 1;
          renderMovies();
        });
      });
    }
  
    // 필터된 영화 반환
    function getFilteredMovies() {
      if (selectedGenres.length === 0) return movies;
      return movies.filter(m => selectedGenres.some(g => m.genres.includes(g)));
    }
  
    // 게시글 표시
    function renderMovies() {
      const filtered = getFilteredMovies();
      const start = (currentPage - 1) * PER_PAGE;
      const current = filtered.slice(start, start + PER_PAGE);
  
      movieGrid.innerHTML = '';
      current.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'post-card';
        card.innerHTML = `
          <div class="post-info">
            <h3>${movie.title}</h3>
            <p>${movie.overview}</p>
            <div class="post-meta">
              <span>개봉일: ${movie.release_date}</span>
              <span>평점: ⭐ ${movie.vote_average}</span>
            </div>
            <div class="movie-genres">장르: ${movie.genres}</div>
          </div>
        `;
      
        card.addEventListener('click', () => {
          window.location.href = `/movies/${movie.id}/`;
        });
      
        movieGrid.appendChild(card);
      });
    }
  
    function renderPagination(data) {
      pagination.innerHTML = '';
      const totalPages = Math.ceil(data.length / PER_PAGE);
  
      for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = i === currentPage ? 'current' : '';
        btn.addEventListener('click', () => {
          currentPage = i;
          renderMovies();
        });
        pagination.appendChild(btn);
      }
    }
  
    renderGenreCheckboxes();
    renderMovies();
  });
  
