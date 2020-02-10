import pandas as pd
import numpy as np
import tensorflow as tf
import datetime

# data_path = 'E:\BaiduNetdiskDownload\kuaishou_a_predict'
data_path = 'D:\Download\快手用户活跃度\快手用户活跃度'
register = pd.read_csv(data_path + '\\' + 'user_register_log.txt', sep='\t',names=['user_id', 'register_day', 'register_type', 'device_type'])
launch = pd.read_csv(data_path + '\\' + 'app_launch_log.txt', sep='\t', names=['user_id', 'launch_day'])
create = pd.read_csv(data_path + '\\' + 'video_create_log.txt', sep='\t', names=['user_id', 'create_day'])
activity = pd.read_csv(data_path + '\\' + 'user_activity_log.txt', sep='\t', names=['user_id', 'act_day', 'page', 'video_id', 'author_id', 'act_type'])

print(register.head())

print(launch.head())

print(create.head())

print(activity.head())

# 计算序列长度， 持续时间 = 数据总时间 - 注册时间

register['seq_length'] = 31 - register['register_day']
print(register.head())

# 构建字典存储用户在持续时间内，不同日期的数据
user_queue = {i:[] for i in range(1, 31)}
for index, row in register.iterrows():
    user_queue[row[-1]].append(row[0])      # row[-1]是seq_length, row[0]是user_id

# key 表示序列长度（持续天数）， value表示用户
print(user_queue)


class user_seq:
    def __init__(self, register_day, seq_length, n_features):
        self.register_day = register_day        # 注册日期
        self.seq_length = seq_length            # 持续时间
        self.array = np.zeros([self.seq_length, n_features])    # 构建矩阵：持续天数 * 特征个数， 后续新创建的特征来往里面填充
        self.array[0, 0] = 1                    # 矩阵第一个数据
        self.page_rank = np.zeros([self.seq_length])    #
        self.pointer = 1

    def put_feature(self, feature_number, string):
        for i in string.split(','):
            pos, value = i.split(':')   # 注册后第几天进行登录， 1为指示符
            self.array[int(pos) - self.register_day, feature_number] = 1

    def put_PR(self, string):
        for i in string.split(','):
            pos, value = i.split(':')
            self.page_rank[int(pos) - self.register_day] = value

    def get_array(self):
        return self.array

    def get_label(self):
        self.label = np.array([None] * self.seq_length)
        active = self.array[:, :10].sum(axis = 1)
        for i in range(self.seq_length -7 ):
            self.label[i] = 1 * (np.sum(active[i + 1: i + 8]) > 0)
        return self.label


n_features = 12
data = {row[0]: user_seq(register_day=row[1], seq_length=row[-1], n_features = n_features) for index, row in register.iterrows()}

# 得到每个用户特征列表
# print(data)

# 登陆信息
launch['launch'] = 1 # 每个用户每天登陆次数
launch_table = launch.groupby(['user_id', 'launch_day'], as_index=False).agg({'launch':'sum'})
print(launch_table.head())

def record_to_sequence(table):
    # 得到用户特征列表
    table.columns = ['user_id', 'day', 'value']
    table.sort_values(by=['user_id', 'day'], inplace=True)
    table['string'] = table.day.map(str) + ':' + table.value.map(str)
    table = table.groupby(['user_id'], as_index=False).agg({'string': lambda x : ','.join(x)})
    return table

launch_table = record_to_sequence(launch_table)
print(launch_table.head())

for index, row in launch_table.iterrows():      # 根据登陆信息对用户特征表进行填充
    data[row[0]].put_feature(1, row[1])         # 在指定特征位置上进行填充

# 创作视频信息
create['create'] = 1
create_table = create.groupby(['user_id', 'create_day'], as_index=False).agg({'create':'sum'})
create_table = record_to_sequence(create_table)
for index, row in create_table.iterrows():
    data[row[0]].put_feature(2, row[1])

# 用户使用行为特征， 例如点赞，转发等
# 分别对不同欣慰进行统计， 构建6种不同行为特征

for i in range(6):
    act = activity[activity.act_type == i].copy()
    act = act.groupby(['user_id', 'act_day'], as_index=False).agg({'video_id':'count'})
    act = record_to_sequence(act)
    for index, row in act.iterrows():
        data[row[0]].put_feature(i + 3, row[1])


# 产生行为的界面信息
for i in range(1):      # 暂不作为特征
    act = activity[activity.page == 1].copy()
    act = act.groupby(['user_id', 'act_day'], as_index=False).agg({'video_id': 'count'})
    act = record_to_sequence(act)
    for index, row in act.iterrows():
        data[row[0]].put_feature(i + 9, row[1])

# 观看其他用户作品信息
watched = register.loc[:, ['user_id']].copy()
watched.columns = ['author_id']
watched = pd.merge(watched, activity[activity.author_id != activity.user_id], how='inner') # 只得到交集，相当于看别人视频
watched = watched.groupby(['author_id', 'act_day'], as_index=False).agg({'video_id':'count'})
watched = record_to_sequence(watched)
for index, row in watched.iterrows():
    data[row[0]].put_feature(10, row[1])

# 观看自己的作品信息
watched = activity[activity.author_id == activity.user_id].copy()
watched = watched.groupby(['user_id', 'act_day'], as_index=False).agg({'video_id': 'count'})
watched = record_to_sequence(watched)
for index, row in watched.iterrows():
    data[row[0]].put_feature(11, row[1])

# 制作数据标签
# 活跃用户定义为：未来7天内使用过app（在上述任一类型日志中出现过）
# 对用户从注册开始时进行统计，对于每天的数据展开，如果7天后仍有行为产生，则标签为1

label = {user_id: user.get_label() for user_id, user in data.items()}
print(label)

data = {user_id: user.get_label() for user_id, user in data.items()}



# 构建RNN网络模型
with tf.variable_scope('train'):
    # 变量与输入
    lr = tf.placeholder(tf.float32, [], name='learning_rate')

    W_out = tf.get_variable('W_out', [n_hu, 1])
    b_out = tf.get_variable('b_out', [1])

    x = tf.placeholder(tf.float32, [None, None, n_features])
    y = tf.placeholder(tf.float32, [None, None])

    batch_size = tf.shape(x)[0]
    seq_length = tf.shape(x)[1]

    # RNN层
    cell = tf.nn.rnn_cell.GRUCell(n_hu)
    initial_state = cell.zero_state(batch_size, dtype = tf.float32)
    outputs, state = tf.nn.dynamic_rnn(cell, x, initial_state=initial_state)

    # 输出层
    outputs = tf.reshape(outputs, [-1, n_hu])
    logits = tf.matmul(outputs, W_out) + b_out
    logits = tf.reshape(logits, tf.stack([batch_size, seq_length]))

# 选择部分预测结果与标签当做训练损失计算
logits_local_train = logits[:,:-14]
label_local_train = y[:, :-14]

# 设置损失函数
regularizer = tf.contrib.layers.l2_regularizer(0.00001)
penalty = tf.contrib.layers.apply_regularization(regularizer, tf.trainable_variables())

obj_local = tf.losses.sigmoid_cross_entropy(label_local_train, logits_local_train) + penalty
optimizer = tf.train.AdamOptimizer(lr)
step_local = optimizer.minimize(obj_local)

# 选择部分预测结果与标签当做测试损失计算
logits_local_test = logits[:, -8]
label_local_test = y[:, -8]


def train(n_obs=1000, step=1000, lr_feed=0.01):
    date_seq = [31] + list(range(2, 16)) + [16] * 15
    variables = [step_local, obj_local, label_local_train, logits_local_train]

    for i in range(step):
        length, id_list, data_x, data_y = data_generator.next_batch(n_obs)
        _, los, lab, log = sess.run(variables, feed_dict={x:data_x, y:data_y, lr:lr_feed})


sess = tf.Session()
sess.run(tf.global_variables_initializer)

train(n_obs=1000, step=2000, lr_feed=0.01)


def test():
    n_NA = 14
    date_seq = [31] + list(range(2, 16)) + [16] * 15
    variables_1 = [obj_local, logits_local_train, label_local_train]
    variables_2 = [logits_local_test, label_local_test]

    obs_count, cum_loss, correct = 0, 0, 0
    user, prob, real = [], [], []

    # 训练损失
    for length, id_list, data_x, data_y in zip(*data_generator.get_set('train')):
        _obj, _logits_train, _label_train = sess.run(variables_1,
                                                     feed_dict={x: data_x,
                                                                y: data_y,
                                                                lr: 0.001})
        obs_count += (length - n_NA) * len(id_list)
        cum_loss += _obj * (length - n_NA) * len(id_list)
        correct += np.sum((1 * (_logits_train > 0) == _label_train))

    # 测试损失
    for length, id_list, data_x, data_y in zip(*data_generator.get_set('test')):
        _ = sess.run(variables_2,
                     feed_dict={x: data_x,
                                y: data_y,
                                lr: 0.001})

        _logits_test, _label_test = _
        real += list(_label_test)

        user += list(id_list)
        prob += list(1 / (1 + np.exp(-_logits_test.reshape([-1]))))

    # 训练损失
    print('train_loss', cum_loss / obs_count)

    # 测试损失
    result = pd.DataFrame({'user_id': user, 'prob': prob, 'label': real})
    print('test_score:', f(result))

    return result


print(test())

