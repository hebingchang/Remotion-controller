// main.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    power: 0,
    temperature: 16,
    mode: 0,//0冷,1热,2除湿
    url: 'http://192.168.78.1:3000/?cmd='
  },

  powerchange: function() {
    var that = this
    if (that.data.power == 1){
      that.setData({
        power: 0
      })
    } else if (that.data.power == 0) {
      that.setData({
        power: 1
      })
    }
  },

  power: function() {
    var that = this
    that.powerchange();
    var power = that.data.power
    var temperature = that.data.temperature
    var mode = that.data.mode
    that.setData({
      url: 'http://192.168.78.1:3000/?cmd=c0_00&power=' + power + '&temperature=' + temperature + "&mode=" + mode
    })
    console.log(that.data.url)
    that.SendData()
  },

  Up_arrow: function () {
    var that = this
    if(that.data.power == 1){
      var power = that.data.power
      var mode = that.data.mode
      var temp = that.data.temperature + 1
      if( temp > 30){
        temp = 30
      }
      that.setData({
        url: 'http://192.168.78.1:3000/?cmd=c0_01&power=' + power + '&temperature=' + temp + "&mode=" + mode,
        temperature: temp
      })
      that.SendData()
    }
  },

  Down_arrow: function () {
    var that = this
    if (that.data.power == 1) {
      var power = that.data.power
      var mode = that.data.mode
      var temp = that.data.temperature - 1
      if (temp < 16) {
        temp = 16
      }
      that.setData({
        url: 'http://192.168.78.1:3000/?cmd=c0_02&power=' + power + '&temperature=' + temp + "&mode=" + mode,
        temperature: temp
      })
      that.SendData()
    }
  },

  modeTap: function(){
    var that = this
    if (that.data.power == 1) {
      var mode = that.data.mode
      if(mode==2){
        mode = 0
      }else{
        mode++
      }
      that.setData({
        mode: mode
      })
      that.SendData()
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
  
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  },

  SendData: function () {
    var that = this
    var JSON = {}
    wx.request({
      url: that.data.url,
      data: {
        
      },
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      success: function (res) {
        // success
        JSON = res.data;
        console.log(JSON);
      },
      fail: function () {
        // fail
        that.setData({
          reminder: '信号发射失败'
        })
      },
      complete: function () {
        // complete
      }
    })
  },
})