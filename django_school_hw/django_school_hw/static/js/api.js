const api_url = "http://127.0.0.1:8000/api/v1/teachers/";
async function getTeacher() {

      const response = await fetch(api_url);
      const data = await response.json();

      for (let i=0; i<data.length; i++) {
          let groups = data[i].group;
          $('#groups').append("<td></td>");

          if (groups.length !== 0){
            for (let j = 0;j < groups.length;j++) {
                $('#groups td').last().append(groups[j].name + ' ' );
        }
          } else {
                $('#groups td').last().append('None');
              }

          $('#name').append("<td>" + data[i].name + "</td>");
          $('#age').append("<td>" + data[i].age + "</td>");
          $('#email').append("<td>" + data[i].email + "</td>");
      }
    }

getTeacher();