// 1. DOMContentLoaded 이벤트로 전체 코드 감싸기
document.addEventListener("DOMContentLoaded", function () {
  // 2. 변수 정의 (한 번만 정의)
    const POSTS_PER_PAGE = 10;
    let posts = [];
    let currentPage = 1;
    let searchKeyword = "";
  
    const postList = document.getElementById("postList");
    const pageButtons = document.getElementById("pageButtons");
    const prevBtn = document.getElementById("prevGroup");
    const nextBtn = document.getElementById("nextGroup");
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
  
      // 3. 게시글을 서버에서 가져오는 함수
async function fetchPosts() {
      try {
          const response = await fetch('/api/posts/');
          if (!response.ok) {
              throw new Error('네트워크 응답에 문제가 있습니다.');
          }
          const data = await response.json();
          posts = data;  // 서버에서 받은 게시글 리스트
          renderPosts(posts); // 데이터 다 받아오면 화면에 보여줌
      } catch (error) {
          console.error('게시글 불러오기 실패:', error);
      }
   }

    // function generateDummyPosts() { //실제 데이터로 수정할 필요가 있습니다. 똑같이 자체 생성한 더미 데이터입니다.
    //   return Array.from({ length: 200 }, (_, i) => ({
    //     id: i + 1,
    //     title: `게시글 제목 ${i + 1}`,
    //     writer: `작성자 ${((i % 5) + 1)}`,
    //     date: `2025-04-${(i % 30 + 1).toString().padStart(2, '0')}`,
    //   }));
    // }
  
    // posts = generateDummyPosts();

  

    function renderPosts() {
      const filtered = posts.filter(post =>
        post.title.toLowerCase().includes(searchKeyword.toLowerCase())
      );
  
      const totalPages = Math.ceil(filtered.length / POSTS_PER_PAGE);
      const startIdx = (currentPage - 1) * POSTS_PER_PAGE;
      const currentPosts = filtered.slice(startIdx, startIdx + POSTS_PER_PAGE);
  
      postList.innerHTML = "";
  
      currentPosts.forEach(post => {
        const item = document.createElement("div");
        item.className = "post-item";
        item.innerHTML = `
          <div class="post-id">${post.id}</div>
          <div class="post-title">
            <a href="/post/${post.id}/"><h3>${post.title}</h3></a>
          </div>
          <div class="post-writer">${post.writer}</div>
          <div class="post-date">${post.date}</div>
        `;
        postList.appendChild(item);
      });
  
      renderPaginationButtons(totalPages);
    }
  

    function renderPaginationButtons(totalPages) {
      pageButtons.innerHTML = "";
  
      const startPage = Math.floor((currentPage - 1) / 10) * 10 + 1;
      for (let i = 0; i < 10; i++) {
        const page = startPage + i;
        if (page > totalPages) break;
  
        const btn = document.createElement("button");
        btn.textContent = page;
        if (page === currentPage) btn.classList.add("active");
        btn.addEventListener("click", () => {
          currentPage = page;
          renderPosts();
        });
        pageButtons.appendChild(btn);
      }
    }
  

    prevBtn.addEventListener("click", () => {
      const prevGroupStart = Math.floor((currentPage - 1) / 10 - 1) * 10 + 1;
      currentPage = prevGroupStart > 0 ? prevGroupStart : 1;
      renderPosts();
    });
  

    nextBtn.addEventListener("click", () => {
      const filtered = posts.filter(post =>
        post.title.toLowerCase().includes(searchKeyword.toLowerCase())
      );
      const totalPages = Math.ceil(filtered.length / POSTS_PER_PAGE);
      const nextGroupStart = Math.floor((currentPage - 1) / 10 + 1) * 10 + 1;
      currentPage = nextGroupStart <= totalPages ? nextGroupStart : currentPage;
      renderPosts();
    });
  

    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        searchKeyword = searchInput.value;
        currentPage = 1;
        renderPosts();
      }
    });
  

    searchButton.addEventListener("click", function () {
      searchKeyword = searchInput.value;
      currentPage = 1;
      renderPosts();
    });
  
  fetchPosts();
});