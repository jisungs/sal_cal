// 급여명세서 자동생성기 웹 버전 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitSpinner = document.getElementById('submitSpinner');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // UI 초기화
            errorMessage.classList.add('d-none');
            successMessage.classList.add('d-none');
            submitBtn.disabled = true;
            submitText.textContent = '처리 중...';
            submitSpinner.classList.remove('d-none');

            const formData = new FormData(uploadForm);
            const fileInput = document.getElementById('file');
            
            // 파일 검증
            if (!fileInput.files || fileInput.files.length === 0) {
                showError('파일을 선택해주세요.');
                resetForm();
                return;
            }

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    // 성공 시 결과 페이지로 리다이렉트
                    window.location.href = data.redirect;
                } else {
                    showError(data.error || '파일 업로드 중 오류가 발생했습니다.');
                    resetForm();
                }
            } catch (error) {
                console.error('Error:', error);
                showError('서버와의 통신 중 오류가 발생했습니다.');
                resetForm();
            }
        });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
    }

    function resetForm() {
        submitBtn.disabled = false;
        submitText.textContent = '생성하기';
        submitSpinner.classList.add('d-none');
    }
});

