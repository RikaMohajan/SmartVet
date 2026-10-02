async function searchDisease(animal) {

    const checkedSymptoms = document.querySelectorAll(".symptoms input:checked");

    let symptoms = [];

    checkedSymptoms.forEach(function(item){
        symptoms.push(item.value);
    });

    if(symptoms.length === 0){
        alert("Please select at least one symptom. / অন্তত একটি লক্ষণ বেছে নিন।");
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

        const result = document.getElementById("result");

        result.innerHTML = "";

        if(data.status == "success"){

            data.results.forEach(function(d){

                result.innerHTML += `
                <div class="result-card">

                    <h2><i class="fa-solid fa-virus"></i> ${d.disease}${d.disease_bn ? " / " + d.disease_bn : ""}</h2>

                    <div class="match">${d.match}% Match / মিল</div>

                    <p>
                        <strong><i class="fa-solid fa-file-lines"></i> Description / বর্ণনা</strong><br>
                        ${d.description}<br>
                        ${d.description_bn || ""}
                    </p>

                    <p>
                        <strong><i class="fa-solid fa-kit-medical"></i> What to do / করণীয়</strong><br>
                        ${d.treatment}<br>
                        ${d.treatment_bn || ""}
                    </p>

                    <p>
                        <strong><i class="fa-solid fa-shield-heart"></i> Prevention / প্রতিরোধ</strong><br>
                        • Vaccinate animals regularly. / নিয়মিত টিকা দিন।<br>
                        • Keep the farm clean and hygienic. / খামার পরিষ্কার রাখুন।<br>
                        • Isolate sick animals immediately. / অসুস্থ প্রাণী সঙ্গে সঙ্গে আলাদা করুন।<br>
                        • Provide clean food and water. / পরিষ্কার খাবার ও পানি দিন।
                    </p>

                </div>
                `;

            });

        }
        else{

            result.innerHTML = `
            <div class="result-card">
                <h2>No Disease Found / কোনো রোগ পাওয়া যায়নি</h2>
                <p>No matching disease found for these symptoms.<br>এই লক্ষণগুলোর সাথে মেলে এমন কোনো রোগ পাওয়া যায়নি। পশুচিকিৎসকের পরামর্শ নিন।</p>
            </div>
            `;

        }

    }
    catch(error){
        console.log(error);
        alert("Server Error / সার্ভারে সমস্যা হয়েছে");
    }

}