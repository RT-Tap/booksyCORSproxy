const getReviews = async() => {
    //development
    //const response = await fetch('http://127.0.0.1:5000/booksyreviews', {method: 'GET',})
    //production
    const response = await fetch('https://booksyAPItest.com/api/booksyreviews', {method: 'GET',}) 
    const data = await response.json()

    const revRef = document.querySelector(".booksy-testimonials")

    revRef.innerHTML = ''; // clear the place holder card
    const reviewnumbers = (window.innerWidth < 800) ? 3 : 5
    for(let i=1; i<reviewnumbers; i++){

        const card = document.createElement("div")
        card.classList.add('booksycard')
        card.setAttribute('id',`card${i}`)
        
        const cardContentDiv = document.createElement("div")
        cardContentDiv.classList.add('card-content')

        card.append(cardContentDiv)

        const starscontainer = document.createElement("div")
        starscontainer.classList.add('star-rating-container');

        const commentDiv = document.createElement("div")
        commentDiv.classList.add("comment")
        const commentref = document.createElement("p")
        commentref.append(data['reviews'][i]['review'])
        commentDiv.append(commentref)

        const reviewerDiv = document.createElement("div")
        reviewerDiv.classList.add("reviewer-name")
        const reviwerRef = document.createElement("h3")
        reviwerRef.append(`${data['reviews'][i]['user']['first_name']} ${data['reviews'][i]['user']['last_name']}`)
        reviewerDiv.append( reviwerRef)

        const rating = data['reviews'][i]['rank']
        for(let i=0; i<5; i++){
            const star = document.createElement("p");
            star.setAttribute('id',`star${i+1}`)
            const starcontent = (rating < i + 1)? document.createTextNode("\u{2606}"): document.createTextNode("\u{2605}");
            star.appendChild(starcontent);
            starscontainer.appendChild(star);
        }
        cardContentDiv.append(starscontainer)
        cardContentDiv.append(commentDiv)
        cardContentDiv.append(reviewerDiv)
        revRef.append(card)
    }
}
console.log("module loaded")
getReviews();