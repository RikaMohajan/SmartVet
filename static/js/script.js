async function searchDisease(animal) {

    const checkedSymptoms = document.querySelectorAll(".symptoms input:checked");

    let symptoms = [];

    checkedSymptoms.forEach(function(item){
        symptoms.push(item.value);
    });

    if(symptoms.length === 0){
        alert("Please select at least one symptom.");
        return;
    }

    try{

        const response = await fetch("/search_disease",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

           body:JSON.stringify({
    animal: animal,
    symptoms: symptoms
})

        });

        const data = await response.json();

        const result=document.getElementById("result");

        result.innerHTML="";

        if(data.status=="success"){

            data.results.forEach(function(d){

                result.innerHTML+=`

               <div class="result-card">

    <h2>🦠 ${d.disease}</h2>

    <div class="match">
        ${d.match}% Match
    </div>

    <p>
        <strong>📝 Description</strong><br>
        ${d.description}
    </p>

    <p>
    <strong>🛡 Prevention</strong><br>
    • Vaccinate animals regularly.<br>
    • Keep the farm clean and hygienic.<br>
    • Isolate sick animals immediately.<br>
    • Provide clean food and water.
</p>

</div>
                `;

            });

        }

        else{

            result.innerHTML=`

            <div class="result-card">

            <h2>No Disease Found</h2>

            <p>No matching disease found.</p>

            </div>

            `;

        }

    }

    catch(error){

        console.log(error);

        alert("Server Error");

    }

}