const surl = "/yts_query"
download_mp3="/dwnlo_mp3"
var app = new Vue({
  delimiters:['${', '}'],
  el: '#app',
  data: {
    user_input:'',
    response_data : {}
  },
  methods : {
    handleSubmit() {
    axios.get(surl+'?q='+this.user_input).then(response => {
        this.response_data=response.data
    })
    },
    download_audio (event) {
    target_id=event.currentTarget.id;
    axios.get(download_mp3+'?vid='+target_id).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data], {type: 'audio/mpeg'}));
        const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', target_id+'.mp3'); //or any other extension
            document.body.appendChild(link);
            link.click();
    })
    }
  }
})

// thumbnails.medium.url || title