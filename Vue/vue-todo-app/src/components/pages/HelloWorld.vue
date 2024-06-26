// Example in a Vue component
<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    axios.get('http://localhost:8000/') // Replace with your API endpoint
      .then(response => {
        this.message = response.data.message;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
}
</script>
