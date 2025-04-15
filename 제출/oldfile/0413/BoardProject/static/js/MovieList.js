document.addEventListener('DOMContentLoaded', function () {
  const PER_PAGE = 8;
  let movies = [];
  let currentPage = 1;
  let selectedGenres = [];

  const movieGrid = document.getElementById('movieGrid');
  const pagination = document.getElementById('pagination');
  const genreForm = document.getElementById('genreForm');

  // 더미 데이터를 fetch형태로 받아오는 함수.
  async function fetchMovies() {
    try {
      const response = await fetch('/movies/api/');
      if (!response.ok) {
        console.error('API 응답 오류:', response.status);
        throw new Error('영화 데이터를 불러올 수 없습니다.');
      }
      const data = await response.json();
      console.log('불러온 데이터:', data);  // 디버깅용
      
      // 장르 문자열 배열로 변환
      return data.movies.map(movie => ({
        ...movie,
        genres: movie.genres || ''  // genres가 null인 경우 대비
      }));
    } catch (error) {
      console.error('데이터 불러오기 실패:', error);
      return [];
    }
  }

  // 장르 필터 체크박스 렌더링
  function renderGenreCheckboxes(allGenres) {
    genreForm.innerHTML = '';
    allGenres.forEach(genre => {
      // 빈 문자열이면 건너뛰기
      if (!genre.trim()) return;
      
      const id = `genre-${genre.replace(/\s+/g, '-')}`;
      genreForm.innerHTML += `
        <label>
          <input type="checkbox" value="${genre}" id="${id}">
          ${genre}
        </label>
      `;
    });

    genreForm.querySelectorAll('input[type="checkbox"]').forEach(input => {  // 게시글 이동까지로 js로 처리합니다.
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
    return movies.filter(m => {
      // 장르가 없거나 빈 문자열이면 필터링하지 않음
      if (!m.genres) return false;
      
      // 선택된 장르 중 하나라도 포함되어 있는지 확인
      return selectedGenres.some(g => m.genres.includes(g));
    });
  }

  // 영화 렌더링
  function renderMovies() {
    const filtered = getFilteredMovies();
    const start = (currentPage - 1) * PER_PAGE;
    const current = filtered.slice(start, start + PER_PAGE);

    movieGrid.innerHTML = '';
    
    if (current.length === 0) {
      movieGrid.innerHTML = '<div class="no-results">검색 결과가 없습니다.</div>';
      return;
    }
    
    current.forEach(movie => {
      const card = document.createElement('div');
      card.className = 'post-card';
      card.innerHTML = `
        <div class="post-info">
          <h3>${movie.title}</h3>
          <p>${movie.overview.length > 100 ? movie.overview.substring(0, 100) + '...' : movie.overview}</p>
          <div class="post-meta">
            <span>개봉일: ${movie.release_date}</span>
            <span>평점: ${movie.vote_average}</span>
          </div>
          <div class="movie-genres">장르: ${movie.genres}</div>
        </div>
      `;

      card.addEventListener('click', () => {
        window.location.href = `/movies/${movie.id}/`;
      });

      movieGrid.appendChild(card);
    });

    renderPagination(filtered);
  }

  // 페이지네이션 렌더링
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

  // 초기 실행
  fetchMovies().then(data => {
    movies = data;
    console.log('처리된 영화 데이터:', movies);  // 디버깅용
    
    // 장르 목록 추출 (콤마로 분리된 문자열을 배열로 변환 후 중복 제거)
    const allGenres = Array.from(new Set(
      movies.flatMap(m => (m.genres || '').split(',').map(g => g.trim()).filter(g => g))
    ));
    
    console.log('추출된 장르:', allGenres);  // 디버깅용
    renderGenreCheckboxes(allGenres);
    renderMovies();
  });
});

  
