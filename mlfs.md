## 多标签数据表

| 序号 | Dataset    | Instances | Features | Labels | class       |
| :--: | ---------- | --------- | -------- | :----: | ----------- |
|  1   | Bibtex     | 7390      | 1836     |  159   | text        |
|  2   | Business   | 5000      | 438      |   30   | text        |
|  3   | Corel5k    | 5000      | 499      |  374   | image       |
|  4   | Emotions   | 593       | 72       |   6    | music       |
|  5   | Enron      | 1702      | 1001     |   53   | text        |
|  6   | Eurlex(ev) | 193480    | 5000     |  3993  | large scale |
|  7   | Health     | 5000      | 612      |   32   | text        |
|  8   | Medical    | 978       | 1449     |   45   | /           |
|  9   | rvc        | /         | /        |   /    | large scale |
|  10  | Scene      | 2407      | 294      |   6    | image       |
|  11  | Yeast      | 2417      | 103      |   14   | biology     |



## 实验

### 数据预处理

最大-最小归一化

### 分类器

MLKNN

参数：

​	neighbor number：10

​	smooth：1

### K折交叉验证

我打算使用5折交叉验证

将数据集划分为10份，做验证时，随机（使用固定的随机种子，确保不同算法的结果可重复）选择1份作为测试集，其他9份作为训练集，然后重复10次，取平均值



### 实验代码框架（仅供参考）

```matlab
% 清理
clear;
clc;

%%
% 指定数据集列表
datasets = {''};
datasets_basepath = '';
result_basepath = '';

%%
% 初始化实验结果记录表
table_header = {'dataset', 'train_size', 'test_size', 'feature_size', 'label_size', 'selected_percent','selected_features_num', 'Hamming Loss', 'Ranking Loss', 'One Error', 'Coverage', 'Average Precision', 'select_time', 'fold_idx'};
result_table = cell(128, length(table_header));
result_table(1, :) = table_header;



% 对每个数据集做实验
for dataset_idx = 1:length(datasets)
	
	
	%%
	% 加载当前数据集
	dataset = datasets{dataset_idx};
	disp(['------------start ',dataset,'---------------']);
	% Todo
	train_data, train_target, test_data, test_target
	%
	
	%%
	% 预处理数据集(ppcd == preprocessed)
	disp(['------------preprcess ',dataset,'---------------']);
	[ppcd_train_data, ppcd_train_target, ppcd_test_data, ppcd_test_target] = preprocess_dataset(dataset, train_data, train_target, test_data, test_target);
	all_data = [ppcd_train_data; ppcd_test_data];
	all_target = [ppcd_train_target; ppcd_test_target];
	
	%%
	% k折实验
	k = 5;
	% 固定随机数种子
	rng(1115);
	indices = crossvalind('Kfold', size(all_data, 1), k);
	
	for fold = 1:k
		disp(['------------start fold ',fold,' ',dataset,'---------------']);
		% 获取当前的训练集索引和测试集索引
		test_idx = (indices == fold);
		train_idx = ~test_idx;
		
		% 划分数据集
		current_train_data = all_data(train_idx, :);
		current_train_target = all_target(train_idx, :);
		current_test_data = all_data(test_idx, :);
		current_test_target = all_target(test_idx, :);
		
		% 特征选择
		tic;
		% Todo
		features_score
		%
		select_time = toc;
		
		% 特征得分降序排名
		[~, sorted_features_score_idx] = sort(features_score, 'descend');
		
		% 按前百分比进行实验评估
		for p = 1:20
			% 选择前百分之p的特征作为挑选的特征子集
			selected_features = sorted_features_score_idx(1:round(p/100 * length(features_score)));
			% 评估(mlfs == multi-label feature selection)
			[Hamming_Loss, Ranking_Loss, One_Error, Coverage, Average_Precision] = mlfs_evaluate(current_train_data, current_train_target, current_test_data, current_test_target, selected_features);
			
			% 记录当前实验结果
			result = {dataset, size(current_train_data, 1), size(current_test_data, 1), size(current_train_target, 2), p, length(selected_features), Hamming_Loss, Ranking_Loss, One_Error, Coverage, Average_Precision, select_time, fold};
			result_table(1+p+(fold-1)*20, :) = result;
			disp(['------------end fold ',fold,' ',dataset,'---------------']);
		end
	end
	% 写入结果到csv文件中
	current_result_path = [result_basepath, dataset, '_result.csv'];
	writecell(result_table, current_result_path);
	disp(['------------end ',dataset,'---------------']);
end
```

