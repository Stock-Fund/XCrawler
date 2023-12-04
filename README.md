# XCrawler

A股爬虫项目

- 核心逻辑1:通过财经网址获取全部股票的动态数据，并且经过分析，将日涨，日跌超过x%的股票进行筛选，按照股票的涨跌幅进行排序；通过对股票的大额买入卖出订单进行排序，并预测前10位买入卖出的之后的大概股价，并对买入卖出进行排序；并存储到数据库(DB:Mysql，需要跟进)

- 核心逻辑2:对保留到数据库的数据按照5日，20日进行分析排序，筛选出5，20日上涨，下降的前x位的股票，进行排序，并存储到数据库(DB:Mysql)

- 核心逻辑3:做T，通过股票的涨跌幅，对股票进行T操作
  1. 使用技术指标建模交易信号。比如利用布林通道、均线交叉等技术分析指标,建立买入和卖出规则。
  2. 加入风险管理作为交易决策依据。比如设置止损价格和动态调整仓位,降低单日风险。
  3. 采用复合指标相结合,避免单一依赖某一指标。比如结合MACD、KDJ等多 time frame 的指标信号。
  4. 进行回测优化,找出参数组合效果好的交易策略。优化周期、触发点设定等策略变量。
  5. 采用平滑移动平均线,避免被短期波动误导。比如用EMA作为买入信号。
  6. 重点跟踪行业领跑股票,利用行业势头。同时观察大盘走势变化。
  7. 使用量化选股条件排除个股风险,比如营收同比增长、获利能力等。
  8. 定期回顾回测结果,调整不好的交易规则。持续优化策略模型。
  9. 采取分散投资多个股票池分担风险。

- 核心逻辑4(分时逻辑):
  1. 通过分析分时大额订单(主力)，小额订单(散户)，来分析当前主力参与程度及后市趋势可能

部分参数解释:

- 上影线(阳线):当日收盘价高于前一日开盘价,形成的阳线称为上影线。
  多次出现上影线表明价格重重阻力难上,预示进一步上涨势头可能受阻。
  长上影线是多空双方经过剧烈拼杀，多方的上攻意愿较强，空方奋力反击形成的K线
- 下影线(阴线):当日收盘价低于前一日开盘价,形成的阴线称为下影线。
  多次出现下影线表明价格受压难支,预示下跌趋势可能加剧。
  长下影线则是空方向下打压意愿较强，多方奋力反击形成的K线
- 上下影线长度要求是K线实体的2-3倍，才可视为长上影线或长下影线，最标准的形态结构是影线是实体的3倍以上。

- SMA(MA)(简单平均数)
  - 普通移动平均线(Moving Average):表示求x在n周期内的简单移动平均
  - 计算方法:n个时间单位移动平均线= (第1个时间单位价格+第2时间单位价格+…+第n时间单位价格)/n
  - 5日均线(5 SMA):是指股票在最近5个交易日(不包括当日)内每日收盘价格的平均值。反映近期价格动向。
  - 10日均线(10 SMA):是指股票在最近10个交易日(不包括当日)内每日收盘价格的平均值。较5日均线则反应的周期稍长。
  - 20日均线(20 SMA):是指股票在最近20个交易日(不包括当日)内每日收盘价格的平均值。相对5日和10日均线,20日均线反映了价格动向的中期趋势。
  - 这三条均线使用不同交易日计算平均价格,周期从短到长。
    - 5日判断近期短中长线价格走势
    - 10日金叉与死叉形成买卖信号
    - 20日价格与不同周期均线的交叉位点形成支持 Resistance 轴。

- EMA(指数移动平均线 EXPMA指标)
  - 通俗说法,EMA则需要给每个时间单位的最高最低等价位数值做一个权重处理，然后再平均,对于越近期的收盘价给予更高的权重，也就是说越靠近当天的收盘价对EMA产生的影响力越大，而越远离当天的收盘价则呈现指数式递减。指数平滑移动平均线的初始值计算方法与简单移动平均相同，也就是将n日间的收盘价的合计除以n算出。然后从第2日起，以前一日的EMA+平滑化常数α×（当日收盘价-前日EMA）算出。此外，平滑化常数为α＝2÷（n+1）。使用此平滑化常数计算，比重就会呈现指数函数性的衰减。相对于SMA来说，EMA走势更为平滑，反映较为灵敏，能更即时反应出近期股价涨跌的波动与转折。但也容易在震荡环境下被主力洗筹的假象给洗出去
  - 指数移动平均线指标(Exponential Moving Average):表示求x在n周期内的平滑移动平均。(指数加权)
  - 计算方法:
    当前周期单位指数平均值 = 平滑系数 * (当前周期单位指数值 - 上一个周期单位指数平均值) + 上一个周期单位指数平均值；
    平滑系数= 2 / (周期单位+1)
    得到：EMA(N) = [ (N-1) * EMA(N-1) + 2 * X(当前周期单位的收盘价)] / (N+1)

- WMA(加权移动平均线)
  - 加权移动平均线指标(Weighted Moving Average):表示求x在n周期内的加权移动平均。在计算平均价格时，对于越近期的收盘价给予越高的权重，而较后期的收盘价则占有较小权重。不过与EMA之间的差异在于，WMA使用的加权乘数是以「线性递减」的方式，与EMA的加权乘数呈现不固定式递减的方式不同。在市场上，WMA这条均线比较少人在使用，绝大多数人还是使用较简单理解的SMA作为主要观察的均线。
  - 计算方法:WMA(N) = [N*第N天收盘价 + (N-1)*第N-1天收盘价 + … + 1*第1天收盘价] / (N+N-1+N-2+....+1)加权乘数总和

- KDJ指标
  - KDJ指标的含义：KDJ是一个动量指标,用于衡量股票近期价格动能的强弱,并判断趋势形成的信号。

  - K值(K)
    1. 衡量最近买势与卖势的相对强度,范围0-100。
    2. K=(C-L14)/(H14-L14)*100
       - C:最近一日收盘价
       - L14:最近14日最低价
       - H14:最近14日最高价

  - D值(D)
    1. K值的简单移动平均,平滑K值的波动。
    2. 当日D = 前一日D值 × (1 - a) + 当日K值 × a (一般a取0.2)

  - J值(J)
    1. 衡量K值与D值距离的平均值,判断K线与D线背离程度。
    2. 当日J = (当日K+前一日K+前一日D)⁄3

  - 指标意义:
    1. K>D表示空头势头较弱或已转弱
    2. K<D表示多头势头较强
    3. K线上穿或下破D线,即K与D背离,可以看作趋势结束或变化的信号

- 布林线指标(Bollinger Bands)
  - 布林线指标是John Bollinger在1986年提出的一种易用且有效的趋势通道指标。是由中轨线和上轨线和下轨线组成。一般可与kdj指标同时分析,得出金叉(起飞信号),死叉(下降信号)信息

  - 布林线指标计算公式:
    - 上轨:20日均线+2倍标准差
    - 中轨:20日均线
    - 下轨:20日均线-2倍标准差
    - 标准差:标准差可以反映一个数据集的离散程度
      - 标准差公式:Σ(收盘价-MA(N日平均线))2/N [N日所有收盘价-N日平均线 所得差开平方的总和 再除以N 得到的结果开根号]
      eg:则:
      Σ(收盘价-MA)2 = (10-15)2 + (11-15)2 + ...+(28-15)2
      Σ(收盘价-MA)2 / 20 = 和/20
      标准差 = √和/20

  - 布林线指标意义:
    1. 由一条20日均线和标准差线组成上下界形成的通道。
    2. 标准差线一般取2倍标准差,表示价格波动98%时间范围内的上下波动空间。
    3. 当价格上行突破上轨或下跌破下轨,反映趋势可能将要改变。
    4. 中轨即20日均线,可以观察价格与均线的关系来判断多空趋势。
    5. 通道越窄,表明价格波动趋于平稳;越宽,则波动动较大。
    6. 价格带来回于通道内,反映短期震荡趋势;一直保持在通道内表现强势趋势。
    7. 常用在趋势判断、震荡发现、买入点挖掘、止损点确定等多种交易策略中。
  - 布林线指标应用:
    - 喇叭口研判:https://www.zhihu.com/question/384284854
      1. 开口型:开口型喇叭口预示着一方力量逐渐强大而一方力量逐步衰竭，价格将处于短期单向行情中，方向则一般由盘整时所处的位置决定，例如高位盘整开口一般意味着暴跌，低位盘整则一般意味着暴涨.
      样子类似喇叭
      开口型喇叭口形态的形成必须具备两个条件。
      其一，长时间的横盘整理，整理时间越长、上下轨之间的距离越小则未来波动的幅度越大；
      其二，布林线开口时要有明显的大的成交量出现。
      开口喇叭口形态的确立是以K线向上突破上轨线、价格带量向上突破中长期均线为准
      2. 收口型:经历上涨后收口型喇叭口预示着空头力量逐渐强大而多头力量开始衰竭，价格将处于短期大幅下跌的行情之中。经历下跌后的收口型喇叭口则相反。收口型喇叭口形态的形成虽然对成交量没有要求。
      样子类似反向喇叭
      收口型喇叭具备一个条件，即价格经过前期大幅的短线拉升，拉升的幅度越大、上下轨之间的距离越大则未来下跌幅度越大。上涨后收口型喇叭口形态的确立是以价格的上轨线开始掉头向下、价格向下跌破短期均线为准。
      3. 紧口型:紧口型喇叭口预示着多空双方的力量逐步处于平衡，价格将处于长期横盘整理的行情中,样子类似3条平行线
      紧口型喇叭口形态的形成条件和确认标准比较宽松，只要价格经过较长时间的大幅波动后，成交极度萎缩，上下轨之间的距离越来越小的时候就可认定紧口型喇叭初步形成。当紧口型喇叭口出现后，投资者既可以观望等待，也可以少量建仓。BOLL线还可以配合判断M头和W底，以W底为例，主要是看左底和右底在布林线中处于何种相对位置上。一般来说，W底的左底会触及下轨线甚至跌破下轨线，但右底却大多是收在布林线下轨线之内，跌破下轨线的时候较少。当价格第一次下跌时，价格跌破布林线下轨线，但随后的反弹却比较强劲，价格不仅越过了布林线的中轨，且能上摸至上轨线；当价格第二次下跌时，没有跌破布林线的下轨线，而是与下轨线有一小段距离，受到下轨线的有力支撑，并再次出现了强劲反弹。从二次下探过程中，我们看到，价格的每次下探是逐步与布林线下轨线拉开距离的，这表明布林线显示市场人气在逐渐地增强，在酝酿着转机。

- RSI指标(相对强弱指数)(动能策略)

  - 指标含义:衡量价格上涨或者下跌动能的技术指标
  - 计算公式:RSI＝[上升平均数÷(上升平均数＋下跌平均数)]×100
    - 上升平均数:N日价格的上涨平均数
    - 下跌平均数:N日价格的下跌平均数
  - 应用:RSI最基本的用法是在指标自下而上突破30点时寻找买入，或者在指标自上而下跌破70时卖出。 该策略是押注市场行情会在强弱间切换，当趋势过强时去捕捉向下的转折点，而当趋势太弱时定位向上的突破机会

- OBV能量潮指标
  - 指标含义:OBV能量潮OBV又称为平衡交易量,它的计算方法是人为的按照股价涨跌赋予成交量为正负数,并进行累加操作,其计算得出的数值并没有什么实际意义,但是其趋势方向的变化却很关键,其和K线形态结合起来运用就更加准确,所以OBV是一个不错的猎庄工具,其变动的方向是重要的参考指标.
  - 计算公式: OBV ＝ 前一日OBV+今日成交量 （如果当日收盘价高于前日收盘价取正值，反之取负值，平盘取零！！！）
  - 指标应用
     1. 股价上升而OBV线下降,表示买盘无力,股价可能会回跌
     2. 股价下降而OBV线上升,表示买盘旺盛,逢低接手强股,股价可能会止跌回升.
     3. OBV线缓慢上升,表示买气逐渐加强,为买进信号
     4. OBV线急速上升,表示力量将用尽为卖出信号
     5. OBV线从正的累加数转为负数,为下跌趋势,投资者应该卖出持有股票.反之OBV线从负的累加数转为正数,应买进股票
     6. OBV线最大的用处,在于观察股价横盘整理后,何时会脱离盘整,以及突破后的未来走势.
     7. OBV线对双重顶第二个高峰的确定有较为标准的显示,当股价自双重顶第一个高峰下跌又再次回升时,如果OBV线能够随股价同步上升且价量配合,则可持续多头市场并出现更高峰.相反当股价再次回升时,OBV线未能同步配合,却见下降,则可能形成第二个顶峰,完成双重顶的形态,导致股价反转下跌.即OBV顶背离.
  - 指标缺陷
     1. OBV指标是建立在国外成熟市场上的经验总结,把它移植到国内必然要经过一番改造才行！比如价涨量增,用在A股坐庄的股票上就不灵了.这时股价涨得越高,成交量反而越小.这是因为主力控盘较重,股价在上涨过程中没有获利筹码加以兑现,所以此时股票涨得很疯,但成交量并不增加.OBV自然无法发挥作用.
     2. 另外,涨跌停板的股票也会导致指标失真.由于A股采用涨跌停板的限制,很多股票在连续涨停的时候,由于股民预期后市会继续大涨,往往持股观望,导致出现越长越无量的现象,因为对于那些达到涨跌停板股票,OBV也无法正常发挥作用.
     3. 目前,A股中仍有大量的"坐庄"现象存在,对于中长线庄家而言,需要在股价处于底部的时候尽可能的吸进大量筹码,然后拉到高处派发.在底部收集筹码阶段,必然会由于庄家的买进造成一定的上涨,同时伴随成交量放大,这时候,为了降低吸筹成本,庄家会把小幅上涨的股价向下打压,到底部后继续吸筹.如此反复,直到吸到足够的筹码为止.
     这个过程反映在OBV上,就是股价在底部盘整,而OBV却一波一波走高,形成底部背离形态,需要特别注意的是,大众所掌握的分析方法也有可能被机构利用.就OBV而言,庄家可以在每日盘中吸筹,使成交量增加,收盘时再把股价打成阴线,这样OBV就会往下走,以此来迷惑投资者.要破解这种手段,一个最有效的方法就是选择15分钟或60分钟的OBV线,这样就可以避开庄家释放的烟雾.
     4. OBV用于研判上升趋势,还是不错的,只是在股价进入下降通道之后,OBV一般作为横盘或上升趋势减缓的参考依据.
  - 指标精华
     1. OBV中有很多精华所在,在实战操盘中,可以撇开Y轴的数值不看,仅按其数值所占Y轴比例分为20%,40%,60%,80%,100%五个区域,通常,在大牛市或熊市中,选择半年以上的时间为横坐标X,在箱体整理的行情中侧选择1个月至3个月的时间为横坐标X来观察OBV曲线
     2. OBV线的底背离现象和异常动向,往往对于黑马有着相当明确的指示作用.比如当股价经过大幅的下跌后,OBV值在0~20%的区域内明显止跌回稳,并出现超过一个月以上,近似水平的横向移动时,表面市场正处在一个漫长的盘整期,大部分投资者没有耐心而纷纷离场,然而此时往往预示着做空的能量已慢慢的减少,逢低吸纳的资金已逐渐增强,大行情随时都有可能发生.当OBV值能够有效的向上爬升时,则表明主力收集阶段已经完成,投资者可根据该收集阶段的股价来计算主力吸货阶段的成本价,计算方法为:
     主力成本价=吸货区域的(最高价+最低价)/2
     3. 当OBV指标创新高的时候股价并没有新高,这说明OBV和股价已经走在出背离的走势,在这种情况下,往往后期股价会跟随指标创出新高,但这种背离的情况也要符合多个条件
       - 首先,指标突破的时候,成交量是逐渐放大的,但是股价并没有突破平台高点
       - 其次,股价必须处于低位状态,如果涨得特别高,即使背离恐怕利润也不会太多,所以低位放量必须是最基本的条件.
     4. 用OBV指标做到长期持有股票，最简单的办法就是当OBV线保持在OBVMA(OBV均线)之上是进行持股。利用这种方法,大家可能会拿到一整波行情,虽然OBV会拐头向下,但是不跌破OBV均线就说明依然保持强势区域.
- 马科维茨模型
- MACD策略(Moving Average Convergence Divergence 移动平均线收敛与发散策略)
  - MACD指标含义:通过计算较长时间和较短时间指数移动平均线的差异,来衡量股票近期价格动能的强弱。一般可与kdj指标同时分析,得出金叉(起飞信号),死叉(下降信号)信息
  - MACD指标计算公式:MACD＝(ema12- ema26) / (ema12 + ema26) * 200 + ema12 其中ema12为12日指数移动平均线,ema26为26日指数移动平均线
  
- 均线策略
  - 策略含义:均线策略指根据移动平均线的交叉信号进行买入卖出操作。
  - 策略类型:
    1. 金叉死叉策略
       当短期均线(如5/10日均线)从下方突破长期均线(如20/50/200日均线)形成金叉形态,视为买信号;
       当短期均线从上方下穿长期均线形成死叉形态,视为卖信号。

    2. 双均线策略
       比如利用5日均线和20日均线,当5日均线从下方突破20日均线时买入,5日均线从上方下穿20日均线时卖出。

    3. 三均线策略
       利用3条不同周期(如5、10、20日)均线进行买卖决策。
    4.均线斜率利用比如5日线、10日线和20日线等不同时间周期的移动平均线,计算出它们在一定期间内的斜率大小。
       - 斜率越大,表示该时期内价格变动幅度越大,价格变化越剧烈。
       - 斜率正数表示上涨趋势,值趋大说明上涨动力增强;斜率负数表示下跌趋势,值越小表明下跌动能减弱。
       - 不同周期均线斜率可互相对比,如短期均线斜率大于长期均线,预示短期动向向上等。
       - 一般使用5日线和20日线比对,5日线斜率大于0且大于20日线,或5日线转正而20日线维持平稳,预示短期内价格有可能走高
       - 可以绘制成柱状图展示不同周期均线斜率高低关系,跟踪趋势变化
- WR(动量策略)
  - 策略含义:WR指标是衡量市场动量的技术指标。WR指标由Williams %R指标和动量指标(MOM)构成。
    1. 该指标能及早发现行情的转向信号，对突发事件反应灵敏，是短线操作应用指标。在使用过程中，最好能结合强弱指数，动向指数等较为平衡的技术指标一起研制，由此可对行情趋势得出较准确的判断。
    2. 超买、超卖和买卖信号非常清楚，能使投资者了解；发出的超卖信号不等于可以买进，而是告知投资者在此价位不要盲目追卖。反之，发出的超买信号也不等于可以卖出，而是警告投资者不要盲目在此价位追买。
    3. 改变W%R曲线的取样天数可以滤除短线频繁的交叉点买卖信号。
    4. 在使用该指标时，会出现超买之后又超买，超卖之后又超卖现象，常使投资者左右为难，不知如何是好。
  - 计算公式: (N周期内最高价-当前价)/(N周期内最高价-N周期内最低价)*100 其中N一般为4或14。
    取值范围为0-100:
    WR值越大,当前价格距离周期最高价越近,表明动能较强;
    WR值越小,当前价格距离周期最低价越近,表明动能较弱。
  - 判断条件
    1、当威廉指标在20——0区间内时，是指标提示的超买区，表明市场处于超买状态，可考虑卖出。威廉指标20线，一般看做卖出线。
    2、当威廉指标进入80——100区间内时，是指标提示的超卖区，表明市场处于超卖状态，可考虑买入。威廉指标80线，一般看做买入线。
    3、当威廉指标在20——80区间内时，表明市场上多空双方处于相持阶段，价格处于横盘整理，可考虑观望。
  - 总结:威廉指标可以运用于行情的各个周期的研究判断，大体而言，威廉指标可分为5分钟、15分钟、30分钟、60分钟、日、周、月、年等各种周期，
WR连续几次撞顶（底），局部形成双重或多重顶（底），是卖出（买进）的信号。这样的信号更为可靠

- DMI(动能策略)
  - 策略含义:DMI指标又叫动向指标或趋向指标,其全称叫“Directional Movement Index,简称DMI”,也是由美国技术分析大师威尔斯．威尔德（Wells Wilder）所创造的,是一种中长期股市技术分析方法。
    1. 上升方向线+DI(又称PDI), +DI为黄色线
    2. 下降方向线- DI (又称 MDI), -DI为红色线
    3. 趋向平均值ADX，主要用于对趋势的判断, ADX为蓝色线
    4. ADXR，对ADX 的评估数值，也是对市场的评估指标, ADXR为绿色线
  - 策略原理:DMI指标是通过分析股价在涨跌过程中买卖双方力量均衡点的变化情况,即多空双方的力量的变化受价格波动的影响而发生由均衡到失衡的循环过程,从而提供对趋势判断依据的一种。
　　DMI指标的基本原理是在于寻找股价涨跌过程中,股价藉以创新高价或新低价的功能,研判多空力量,进而寻求买卖双方的均衡点及股价在双方互动下波动的循环过程。在大多数指标中,绝大部分都是以每一日的收盘价的走势及涨跌幅的累计数来计算出不同的分析数据,其不足之处在于忽略了每一日的高低之间的波动幅度。比如某个股票的两日收盘价可能是一样的,但其中一天上下波动的幅度不大,而另一天股价的震幅却在10%以上,那么这两日的行情走势的分析意义决然不同,这点在其他大多数指标中很难表现出来。而DMI指标则是把每日的高低波动的幅度因素计算在内,从而更加准确的反应行情的走势及更好的预测行情未来的发展变化。
  - 计算正向动量指标DI+: DI+ = (当日高点 - 上一日高点)/当日移动范围 × 100
  - 计算负向动量指标DI-: DI- = (当日低点 - 上一日低点)/当日移动范围 × 100
  - 移动范围: 每日最高价 - 每日最低价 移动范围是用来标准化DI+和DI-的值,消除因价格范围不同而引起的指标计算误差
  - 计算动向指标DM: DM+ = DI+的N日简单移动平均  DM- = DI-的N日简单移动平均
  - 计算动向趋势线DX: DX = abs(DM+)/ (abs(DM+)+abs(DM-)) * 100
  - 计算动向移动平均指数DMI: DMI = N日EMA(DX)
  - 计算公式:
  - 参考逻辑:
    1. 多空指标包括(+DI多方、-DI空方 +DM多动向、-DM空动向)
       - +DI在-DI上方,股票行情以上涨为主
       - +DI在-DI下方，股票行情以下跌为主
       - 在股票价格上涨行情中，当+DI向上交叉-DI，是买进信号，相反,当+DI向下交叉-DI，是卖出信号。
       - -DI从20以下上升到50以上,股票价格很有可能会有一波中级下跌行情。
       - +DI从20以下上升到50以上,股票价格很有可能会有一波中级上涨行情。
       - +DI和-DI以20为基准线上下波动时，该股票多空双方拉锯战,股票价格以箱体整理为主。
       - 当ADX脱离20－30之间上行，不论当时的行情是上涨或下跌，都预示股价将在一段时间维持原先的走势。
       - 当ADX位于＋DI与－DI下方，特别是在20之下时，表示股价已经陷入泥沼，应远离观望
       - 当绿色的ADXR曲线低于20时，所有指标都将失去作用，应果断离市。
       - 在一般的行情中，ADX的值高于50以上时，突然改变原来的上升态势调头向下，无论股价正在上涨还是下跌都代表行情即将发生反转。此后ADX往往会持续下降到20左右才会走平。但在极强的上涨行情中ADX在50以上发生向下转折，仅仅下降到40－60之间，随即再度回头上升，在此期间，股价并未下跌而是走出横盘整理的态势。随着ADX再度回升股价向上猛涨，这种现象称为"半空中转折"。也是大行情即将来临的征兆。但在实际操作中仍遵循ADX高于50以上发生向下转折，即抛出持股离场观望，在确认"半空中转折"成立后再跟进的原则
       - 当＋DI与-DI相交之后，ADX会随后与ADXR交叉，此时如果行情上涨，将是最后一次买入机会；如果行情下跌，将是最后一次卖出机会。如图所示，白色的+DI上穿黄色的-DI之后不久，紫色的ADX就上穿绿色的ADXR，随即股价开始大幅上扬。
    2. DMI数值 reflects当前趋势的强弱,通常:
       - DMI>50表示趋势明确
       - 两条DM交叉时可能发生趋势转向

- 可转债策略
  - 可转债是一种可以在特定的时间、按特定的转换条件转换为标的股票的公司债券，其本质上就是一个债券+看涨期权的组合。因而，可转债的风险低于股票，高于普通债券。可转债之所以受到中低风险投资者的追捧，是因为其兼具股性与债性，进可攻退可守，安全性较高。另一方面，根据风险与收益率相匹配的原则，可转债的收益率低于股票，但高于普通债券。你不能指望既保本，收益率又高于排名靠前的股票基金。
  - 可转移债的影响:
     1. 股价波动。到期日前后,持有人可能根据股价走势决定是否转换为股票,这会带来一定程度的股价波动。

     2. 股本结构变化。如果部分或全部债券转换为股票,公司股本将相应增加,每股收益可能略有下降。

     3. 普通股增发供应。大批量转换将增加额外股份供应,短期内可能会形成一定的卖压。

     4. 股东基础扩大。通过可转债公司增强了股东群体,并获得新的长期股东支持。

     5. 资金来源渠道变多。可转债到期后公司将获得债券发行所得资金,对其进一步发展有帮助。

     6. 市场关注度升高。到期日通常股价波动大,也将吸引更多投资者重点关注该股票。

     7. 融资成本下降。通过可转债公司可降低融资成本,提升资金利用率,对后期经营有利
  - 操作
     1. 股票价格上涨时转换:
        - 可以按较低的转换价格参与公司更高价值。
        - 但此时股价可能会因为供应增加而下跌。
     2. 股票价格下跌时转换:
        - 可以利用低价入市股票
        - 但如果股价继续下跌,将承受更大亏损。
     3. 一般来说
        - 转换价格高于股票价格时,转换成本较高。
        - 当转入大量股票后,会增加股票的流通数量，引起股东结构和控股比例的调整,带来风险
        - 如果市场上可转债过多,会对股票带来一定抛售压力
- 资金流策略
