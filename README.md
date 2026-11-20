# 课程组合退款差额与商家对账

各表为本地合成业务记录，身份与机构代号不对应真实对象。

## 资料格式

资料为 UTF-8 编码、首行为列名的 CSV。空字段表示没有记录，不表示零。连续日号采用同一份内部日历。

| 文件 | 列 | 登记口径 |
| --- | --- | --- |
| `quotes.csv` | `line`、`order`、`category`、`merchant`、`gross`、`paid_weight` | 分项报价与订单内的实付拆分约定，金额均为分；按相对权重，尾差留在同一分项的结算责任内。 |
| `payments.csv` | `pay`、`order`、`leg`、`channel`、`received`、`amount` | 跨期支付，不把报价当已收款。 |
| `awards.csv` | `case`、`revision`、`line`、`pay`、`payer`、`amount`、`status`、`known`、`period` | 裁决可拆给多付款方；同 case 和 revision 的多条记录共同生效。 |
| `movements.csv` | `id`、`pay`、`payer`、`chan_ref`、`case_hint`、`state`、`amount`、`known`、`prior` | 资金流水和对方引用，case_hint 未经确认不能作为合并依据；prior 为被冲正流水。 |
| `confirmations.csv` | `id`、`observed`、`canonical`、`case`、`known`、`state` | 独立渠道归并与核对回执，same 不增加一笔出款。 |
| `signed_lines.csv` | `report`、`line`、`case`、`party`、`period`、`payable`、`issued`、`signed` | 原对账报表中以尚待出款口径签收的行，金额不是历史资金流。 |
| `cycles.csv` | `period`、`effective`、`asof`、`state` | 结算批次与当次所见材料时点。 |
| `clearing.csv` | `batch`、`channel`、`date`、`net_cents`、`declared_fee`、`fee_party`、`known` | 外部清算净额保留方向，正数为本金流出、负数为回流，费用为独立带正号的渠道支出；批次金额不是某笔订单的材料。 |
| `clear_evidence.csv` | `batch`、`candidates`、`known`、`classification` | possible 表示该批可含这些流水的某个组合（并非全取）；bank_confirmed 为独立渠道确认。真实为同笔的流水不能解释两次本金流。 |
| `dispatch.csv` | `dispatch`、`adjustment`、`batch`、`case`、`payer`、`amount`、`known`、`state` | 批级收件不能使每行生效；调整方向由与原单的差额而定。这张表为一次本地向财务发送的独立回执，不能代替银行付款。 |

## 检查资料

使用 Python 3.11 和标准库。在项目根目录运行：

```sh
python3 -m unittest discover -s tests -v
```

这项检查核对资料格式与引用，不生成业务结论。
