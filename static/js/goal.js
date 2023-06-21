function getImageFiles(e) {
    const file = e.currentTarget.files[0];
    const uploadImage = document.querySelector('.goal-preview-images');

    console.log(typeof file, file)

    const reader = new FileReader();
    reader.onload = (e) => {
        console.log(e);
        uploadImage.setAttribute('src', e.target.result);
        uploadImage.setAttribute('data-file', file.name)

    }
    reader.readAsDataURL(file)
}

const uploadImageInput = document.querySelector('.goal-images-input');
uploadImageInput.addEventListener('change', getImageFiles);