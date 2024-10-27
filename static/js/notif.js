let toastBox =document.getElementById('toastBox');
const maxToastCount = 3; // Maksimal toast
function showToast(header, msg, isSuccess = true) {
    // Validasi untuk hapus toast yang paling lama
    if (toastBox.children.length >= maxToastCount) {
        toastBox.removeChild(toastBox.firstChild);
    }

    // Buat elemen toast baru
    let toast = document.createElement('div');
    toast.classList.add('toast');
    if (!isSuccess) {
        toast.classList.add('deleted'); // Tambahkan kelas deleted jika status bukan success
    }

    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${isSuccess ? 'fa-check' : 'fa-xmark'} check"></i>
            <div class="message">
                <span class="text text-1">${isSuccess ? header : 'Deleted'}</span>
                <span class="text text-2">${msg}</span>
            </div>
        </div>
        <i class="fa-solid fa-xmark close" onclick="this.parentElement.remove()"></i>
        <div class="progress ${isSuccess ? 'active' : 'deleted'}"></div>
    `;

    toastBox.appendChild(toast);

    // Hapus toast setelah beberapa detik
    setTimeout(() => {
        toast.remove();
    }, 3000);
}