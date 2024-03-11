<template>
<div id="app">
    <RadioGroup v-model="language" type="button" style="margin-left: 80%;margin-top: 20px;" @on-change="changeLan">
        <Radio label="en">English</Radio>
        <Radio label="cn">简体中文</Radio>
    </RadioGroup>
    <div v-if="language==='en'">
    <row class="upper">
        <Tabs value="name1" >
             
             <TabPane label="Product Search Recommendations" name="name1">
                 
                 <Row style="background:#eee;padding: 20px" >
                    <Col span="12">
                        <Input @on-search="handlePro" v-model="search1" search enter-button="Search" placeholder="Enter something..." />
                    </Col>
                 </Row>
       
                 <Row> <div style="background:#eee;padding: 20px">
               
                    <Spin size="large" fix v-if="spinShow" ></Spin> {{productInfo}}
                 </div>
                 </Row>
                 
               </TabPane>
               <TabPane label="Product Review Analysis" name="name2">
                 <Row style="background:#eee;padding: 20px" >
                    <Col span="12">
                        <Input @on-search="handleSmg" v-model="search2"  search enter-button="Analysis" placeholder="Enter something..." />
                    </Col>
                 </Row>
       
                 <Row> 
                 <div style="background:#eee;padding: 20px">
               
                  <Spin size="large" fix v-if="spinShow"></Spin>{{pmsInfo}}
                 </div>
                 </Row>
               </TabPane>
               
           </Tabs>
    </row>
    <row class="lower">
        <div style="padding: 10px"><b  style="font-size: 16px;">Product List</b></div>
        <Col span="16" style="overflow-y: auto; height: calc(100vh - 50px);" >
            <Card :bordered="false" v-for="(item,index) in proItems" :key="index">
                <p slot="title">
                    {{item.ProductID}}: {{item.ProductName}}
                </p>
                <p>
               <Tabs value="product" @on-click="changeProductLabel(item.ProductID)">
                <TabPane label="Product Details" name="product">
                
                <row>
                <Col span="12">
                <row><b>Category</b>: {{item.Category}}</row>
                <b>Description</b>: <li v-for="(value, key) in jsonObject(item.Description)" :key="key">
                {{ key }}: {{ value }}
                </li>
                <b>Reviews</b>:
                <Button type="primary" size="small" @click="fetchProductMsData(item)">
                    Reviews
                    <Icon type="ios-arrow-forward"></Icon>
                </Button>
                </Col>
                <Col span="8">
                <img width="300px" :src=item.Image>
                </Col>
              
                </row>
                </TabPane>
                </Tabs>
            </p>
            </Card>
            
        </Col>
        <Col span="8" style="overflow-y: auto; height: calc(100vh - 50px);">
        <div  class="left" v-if="showReviews">
            <div style="margin-bottom: 10px"><b  style="font-size: 16px;">Reviews {{selectProduct.ProductID}}</b></div>
            <div v-for="(item2, index2) in mesItems" :key="index2">
                
                <row><b>{{item2.UserID}}: </b>  {{item2.Comment}} , <b> Rating {{item2.Rating}}</b> , {{formatDate(item2.Timestamp)}}</row> 
                <Divider />
        
            </div>
            
            <row><Rate v-model="rating" /></row> 
            <row> <Input search enter-button="Submit Review" placeholder="Enter something..."  v-model="inputValue" @on-search="addProductMs"/></row>
            
            <Divider />
        </div>
        </Col>

    </row>
    </div>

    <div v-else>
        <row class="upper">
        <Tabs value="name1" >
             
             <TabPane label="商品推荐" name="name1">
                 
                 <Row style="background:#eee;padding: 20px" >
                    <Col span="12">
                        <Input @on-search="handlePro" search enter-button="搜索" placeholder="请输入..." />
                    </Col>
                 </Row>
       
                 <Row> <div style="background:#eee;padding: 20px">
               
                    <Spin size="large" fix v-if="spinShow" ></Spin> {{productInfo}}
                 </div>
                 </Row>
                 
               </TabPane>
               <TabPane label="商品评价分析" name="name2">
                 <Row style="background:#eee;padding: 20px" >
                    <Col span="12">
                        <Input @on-search="handleSmg" search enter-button="分析" placeholder="请输入..." />
                    </Col>
                 </Row>
       
                 <Row> 
                 <div style="background:#eee;padding: 20px">
               
                  <Spin size="large" fix v-if="spinShow"></Spin>{{pmsInfo}}
                 </div>
                 </Row>
               </TabPane>
               
           </Tabs>
    </row>
    <row class="lower">
        <div style="padding: 10px"><b  style="font-size: 16px;">商品列表</b></div>
        <Col span="16" style="overflow-y: auto; height: calc(100vh - 50px);" >
            <Card :bordered="false" v-for="(item,index) in proItems" :key="index">
                <p slot="title">
                    {{item.ProductID}}: {{item.ProductName}}
                </p>
                <p>
               <Tabs value="product" @on-click="changeProductLabel(item.ProductID)">
                <TabPane label="Product Details" name="product">
                
                <row>
                <Col span="12">
                <row><b>分类</b>: {{item.Category}}</row>
                <b>详情</b>: <li v-for="(value, key) in jsonObject(item.Description)" :key="key">
                {{ key }}: {{ value }}
                </li>
                <b>评论</b>:
                <Button type="primary" size="small" @click="fetchProductMsData(item)">
                    查看
                    <Icon type="ios-arrow-forward"></Icon>
                </Button>
                </Col>
                <Col span="8">
                <img width="300px" :src=item.Image>
                </Col>
              
                </row>
                </TabPane>
                </Tabs>
            </p>
            </Card>
            
        </Col>
        <Col span="8" style="overflow-y: auto; height: calc(100vh - 50px);">
        <div  class="left" v-if="showReviews">
            <div style="margin-bottom: 10px"><b  style="font-size: 16px;">评价 {{selectProduct.ProductID}}</b></div>
            <div v-for="(item2, index2) in mesItems" :key="index2">
                
                <row><b>{{item2.UserID}}: </b>  {{item2.Comment}} , <b> 评分 {{item2.Rating}}</b> , {{formatDate(item2.Timestamp)}}</row> 
                <Divider />
        
            </div>
            
            <row><Rate v-model="rating" /></row> 
            <row> <Input search enter-button="提交评论" placeholder="请输入..."  v-model="inputValue" @on-search="addProductMs"/></row>
            
            <Divider />
        </div>
        </Col>

    </row> 
    </div>
</div>
</template>

<script>
import axios from 'axios';
import { Row } from 'iview';
const APIURL = ''
export default {
    data() {
        return {
            search1: '',
            search2: '',
            proItems: [],
            mesItems: [],
            productInfo: '',
            pmsInfo: '',
            spinShow: false,
            showReviews: false,
            language: 'en',
            selectProduct: [],
            rating: 0.0,
            inputValue: '',

        };
    },
    mounted() {
        this.fetchProductData();
    },
    methods: {
        changeLan(value) {
            console.log(value)
            this.spinShow = false;
            this.productInfo = '';
            this.pmsInfo = '';
            this.search1 = '';
            this.search2 = '';
            this.fetchProductData()
        },
        changeProductLabel(value) {
          console.log(value)

        },
        jsonObject(value) {
            try {
                return JSON.parse(value);
            }
            catch (error) {
                console.error('Invalid JSON string:', error);
                return {};
            }
        },
        handlePro(value) {
            if(value === null || value.trim() === '') {
                this.productInfo = ''
                this.fetchProductData()
                return
            }
            this.spinShow = true;
            this.productInfo = '';
            // 发送POST请求
            axios.post(APIURL + '/recomm?type=product_recommend&language='+this.language, {
                input_text: value
            }).then(response => {
                // 处理响应数据
                console.log(response.data);
                this.spinShow = false;
                this.productInfo = 'Results: ' + response.data.llm_result;
                this.proItems = response.data.es_response.hits.hits.map(hit => hit._source);
            }).catch(error => {
                // 处理错误
                console.error(error);
            });
        },
        handleSmg(value) {
            console.log(value)
            this.spinShow = true;
            this.pmsInfo = '';
            // 发送POST请求
            axios.post(APIURL+ '/recomm?type=reviews_analytis&language='+this.language, {
                input_text: value
            }).then(response => {
                // 处理响应数据
                console.log(response.data);
                this.spinShow = false;
                this.pmsInfo = 'Results: ' + response.data.llm_result;
            }).catch(error => {
                // 处理错误
                console.error(error);
            });
        },
        formatDate(timestampInSeconds) {
            const date = new Date(timestampInSeconds * 1000); // 将秒转换为毫秒
            const year = date.getFullYear();
            const month = `0${date.getMonth() + 1}`.slice(-2);
            const day = `0${date.getDate()}`.slice(-2);
            const hours = `0${date.getHours()}`.slice(-2);
            const minutes = `0${date.getMinutes()}`.slice(-2);
            const seconds = `0${date.getSeconds()}`.slice(-2);
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
        fetchProductData() {
            this.proItems = []
            axios.get(APIURL+'/shop?type=get_products&language='+this.language)
                .then(response => {
                this.proItems = response.data;
            })
                .catch(error => {
                console.error(error);
            });
        },
        fetchProductMsData(value) {
            console.log(value)
            this.showReviews = false
            this.selectProduct = value
            axios.get(APIURL + '/shop?type=get_product_reviews&language=' + this.language + '&product_id=' + value.ProductID)
                .then(response => {
                this.showReviews = true
                this.mesItems = response.data;
            })
                .catch(error => {
                console.error(error);
            });
        },
        generateRandomString(length) {
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            let result = '';
            for (let i = 0; i < length; i++) {
                const randomIndex = Math.floor(Math.random() * characters.length);
                result += characters.charAt(randomIndex);
            }
            return result;
        },
        addProductMs(value) {
            console.log(value)
            console.log(this.rating)
            console.log(this.selectProduct)
            console.log(this.generateRandomString(6))
            
            // 发送POST请求
            axios.post(APIURL+ '/shop?type=add_product_review&language='+this.language, 
            {
                'product_id':  this.selectProduct.ProductID,
                'product_name': this.selectProduct.ProductName,
                'rate': this.rating,
                'comment': value,
                'user_id': this.generateRandomString(6)
            }
            ).then(response => {
                // 处理响应数据
                console.log(response.data);
                if(response.data[0] == 'success') {
                    this.$Notice.success({
                    title: 'success'
                });
                this.rating = 0.0
                this.inputValue = ''
                this.fetchProductMsData(this.selectProduct)
                }else {
                    this.$Notice.open({
                        title: 'Faild',
                        duration: 0
                    });
                }
                
            }).catch(error => {
                // 处理错误
                console.error(error);
            });
        },
    },
    components: { Row }
};

</script>

<style module>
.upper {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 100;
}

.left {
    margin-left: 10%;
    margin-right: 10%;
}
</style>


