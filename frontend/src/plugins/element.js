import Vue from 'vue'
import {
  Button,
  Card,
  Form,
  FormItem,
  Radio,
  RadioGroup,
  InputNumber,
  Message,
  Loading,
  Table,
  TableColumn,
  DatePicker,
  Select,
  Option,
  Row,
  Col,
  Timeline,
  TimelineItem,
  Collapse,
  CollapseItem,
  Pagination,
  Container,
  Header,
  Main,
  Footer,
  Menu,
  MenuItem,
  Submenu
} from 'element-ui'

// 基础组件
Vue.use(Button)
Vue.use(Card)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(InputNumber)

// 布局组件
Vue.use(Container)
Vue.use(Header)
Vue.use(Main)
Vue.use(Footer)
Vue.use(Row)
Vue.use(Col)

// 导航组件
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(Submenu)

// 数据展示组件
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Timeline)
Vue.use(TimelineItem)
Vue.use(Collapse)
Vue.use(CollapseItem)
Vue.use(Pagination)

// 表单组件
Vue.use(DatePicker)
Vue.use(Select)
Vue.use(Option)

// 指令
Vue.use(Loading.directive)

// 服务
Vue.prototype.$loading = Loading.service
Vue.prototype.$message = Message 