def sort_single_file():
    all_line = {}
    with open('weibo_data_特征.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if '特征' in line:
                #if '转发活动微博' not in line and '投票活动' not in line and '网页链接活动名称' not in line:
                    all_line[line] = 0

    with open('weibo_data_特征.txt' , 'w' , encoding='utf-8') as f:
        for line in all_line.keys():
            f.write(line)

def sort_all_file():
    final_path = r'D:\wyy\sourcedata\didi\weibo_data.txt'
    single_files = ['weibo_data_城市.txt' , 'weibo_data_活动.txt' , 'weibo_data_交通.txt' , 'weibo_data_游玩.txt' , 'weibo_data_特点.txt' , 'weibo_data_旅游.txt' , 'weibo_data_特征.txt' , 'weibo_data_城市_功能.txt'  , 'weibo_data_区域.txt']
    all_line = {}
    for file in single_files:
        with open(file , 'r' , encoding='utf-8') as f:
            for line in f.readlines():
                if '城市' in line or '活动' in line or '交通' in line or '游玩' in line or '特点' in line or '旅游' in line or '特征' in line or '功能' in line or '区域' in line:
                    line = line.strip().split('\t')
                    if len(line) == 3:
                        all_line[line[2]] = 0

    with open(final_path , 'w' , encoding='utf-8') as f:
        for line in all_line.keys():
            f.write(line + '\n')

if __name__ == '__main__':
    #sort_single_file()
    sort_all_file()