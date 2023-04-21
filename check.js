function activateBtn() {
    const target = document.getElementById('target_btn');
    target.disabled = false;
}

// 파이썬 파일 실행

setInterval(function() {
        // 진행도 확인, html 업데이트
        var element = document.getElementById("progress");
        element.innerText = "진행도";

        if (true) { // 완료 시
            activateBtn();
        }
    }, 1500);
