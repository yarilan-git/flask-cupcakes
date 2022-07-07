setupFormBtnListeners();
showCupcakeList();

function setupFormBtnListeners() {
    $("#cancel").on('click', resetForm);
    $("#add").on('click', addCupcake);
}

async function showCupcakeList() {
    const cupcakes = await axios.get('/api/cupcakes');
    for (const cupcake of cupcakes.data.cupcakes) {
        addCupcakeToList(cupcake);
    }
}

async function addCupcake(e) {
    e.preventDefault();
    if (allInputsAreValid()) {
        const details = {flavor: $("#flavor").val(),
                         size: $("#size").val(),
                         rating: parseFloat($("#rating").val()),
                         image: ($("#image").val()) ? $("#image").val() : 'https://tinyurl.com/demo-cupcake'};
        let res = await axios.post('/api/cupcakes', details);
        addCupcakeToList(res.data.cupcake);
        clearForm();
    }
}

function resetForm(e) {
    e.preventDefault();
    clearForm();
}

function clearForm() {
    $("#size").val('');
    $("#rating").val('');
    $("#image").val('');
    $("#flavor").val('');
    $("#message").addClass("hidden");
}

function allInputsAreValid() {
    $("#message").addClass("hidden");
    if ($("#size").val() == '' ||
        $("#rating").val() == '' ||
        $("#flavor").val() == '') {
            $("#message").text("All of the above information, except image, is required !");
            $("#message").toggleClass("hidden");
            return false;
        }

    if (isNaN($("#rating").val())) {
        $("#message").text("The rating can only be a number!");
        $("#message").toggleClass("hidden");
        return false;
    }

    return true;
}

function addCupcakeToList(cupcake) {
    if (!$("table").length) {
        createTable();
        }
    addOneCupcakeToList(cupcake);
    }

function createTable() {
    const tableElement = 
        `<table>
            <thead>
                <tr>
                    <th>Flavor</th>
                    <th>Size</th>
                    <th>Rating</th>
                    <th>Image</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>`
        $("#cupcake_list").append(tableElement);        
}
    
function addOneCupcakeToList(cupcake) {
    const newRow = 
        `<tr>
            <td>${cupcake.flavor}</td>
            <td>${cupcake.size}</td>
            <td>${cupcake.rating}</td>
            <td><img src=${cupcake.image} onerror="this.src='static/pics/not-found.png'"></td>
            <td class="delete" data-cupcake-id=${cupcake.id}>Delete</td>
        </tr>
        `
    $("tbody").append(newRow);
    // $("td.update").data( "cupcake-id", cupcake.id ).on('click', editCupcake);
    $("td.delete").data( "cupcake-id", cupcake.id ).on('click', deleteCupcake);
}

// async function editCupcake(e) {
//     e.stopImmediatePropagation();
//     alert("Inside edit func");
// }


async function deleteCupcake(e) {
    e.stopImmediatePropagation();
    const id=e.target.getAttribute('data-cupcake-id');
    resp=await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove();
}

