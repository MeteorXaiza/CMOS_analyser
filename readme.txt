取扱説明書


1. 基本的な使い方
  ターミナル上で動かしてください。
  例）python gen_event_list.py -i ./frame_20190901
  引数に「-h」を指定すると、コマンド引数のヘルプが表示されます。
  例）python gen_event_list.py -h
  引数はターミナル上だけでなく、コンフィグファイル(~~.ini)からも指定できます。その際は、引数に「-c [config_file_path]」を指定してください。
  コンフィグファイルは付属したものを使っても構いません。（~~_config.ini）
  例）python gen_event_list.py -c event_list_config.ini
  また、引数はターミナル上での値が優先されます。
  例）
    event_list_config.ini
      [input]
      directory_path = ./frame_20190315/
    ターミナル
      python gen_event_list.py -c event_list_config.ini -i ./frame_20190913/
    コンフィグファイル上では、解析するディレクトリが「./frame_20190315/」に指定されていて、ターミナル上では、「./frame_20190913/」に指定されている。この場合、ターミナルの「./frame_20190913/」が優先され、解析されるディレクトリとなる。
  コマンドライン上でのコマンド「python gen_event_list.py」などを短縮するには、「~/.bashrc」にaliasを追加するのが有効です。
  例）
    .bashrc
      alias gen_event_list='python /Users/MeteorXaiza/Python/HanasakaTest/analysis_set/version_4/gen_event_list.py'
    ターミナル
      gen_event_list -c event_list_config.ini


2. gen_mean_BG_frame_single.py
  バックグラウンドの平均値を求める他、標準偏差や尖度も求め、FITSファイルに保存します。標準偏差は不偏標準偏差（残差二乗和を(サンプル数)-1で割った分散の正の平方根）です。尖度は正規分布のものを0としたものです(μ_4/μ_2^2-3)。
2.1 引数
  --config_file, -c
    コンフィグファイルのパスを指定することで、引数を設定できます。
  --input_directory, -i, (config : [input], directory_path)
    解析するフレームとなるファイルが入ったディレクトリパスを指定できます。何も指定しなければ、カレントディレクトリ「./」を指定したものとみなします。
  --event_list_file, (config : [input], event_list_file_path)
    イベントリストファイルのパスを指定することで、フレームの中にあるイベントを取り除いて解析できます。取り除く範囲はイベントリストファイルのヘッダーのMAXLEAKに依存します。
    例）MAXLEAK=4 => 取り除く範囲 : 9x9ピクセル
    全てのフレームでイベントの範囲となったピクセルは、平均値の解析結果がnanになります。イベントの範囲にならなかったフレーム数が2フレーム未満のピクセルは標準偏差の解析結果がnanになります。「None」を指定、または、何も指定しなければ、フレームの中にイベントはないものとみなし、全てのピクセルが解析に使用されます。
  --limit_frame_num, (config : [input], limit_frame_num)
    解析に使用するフレーム数を指定できます。「None」を指定、または、何も指定しなければ、ファイル名が--match_file_nameでマッチする全てのフレームが解析に使用されます。
  --match_file_name, (config : [input], match_file_name)
    解析するフレームのファイル名を正規表現で指定します。何も指定しなければ、「.+\.fits」を指定したとみなし、ファイル名が「~~.fits」となっているものが解析に使用されます。
  --HDU_index, (config : [input], HDU_index)
    解析するフレームのHDUのインデックスを指定できます。何も指定しなければ、「0」を指定したとみなし、解析します。
  --valid_frame_shape, (config : [input], valid_frame_shape)
    解析するフレームのサイズ（ピクセル数）を指定できます。--input_directoryで指定したディレクトリの中にあるフレームのサイズが混在している場合、--valid_frame_shapeで指定されたサイズのフレームが解析されます。指定の仕方は「[高さ(Yの大きさ)]x[幅(Xの大きさ)]」としてください。
    例）2040x2048
    その他にも、「\d+ *[x|X|,] *\d+」でマッチする文字列ならば構いません。
    例）2040,2048
    「None」を指定、または、何も指定しなければ、--match_file_nameでマッチするファイルのうち、辞書順の一番先頭のファイル名のフレームのサイズを指定したとみなします（その際、一度そのファイルを読み込むことになります）。
  --invalid_shape_process, (config : [input], invalid_shape_process)
    --valid_frame_shapeで指定されたサイズ以外のフレームサイズのフレームを解析しようとした際の処理を指定できます。「first」、「quit」、「select」の3つから指定してください。何も指定しなければ、firstを指定したものとみなします。firstを指定した場合、解析せずにそのフレームを無視します。quitを指定した場合、以降の解析も行わずに解析を完全に終了し、何も出力されません。selectを指定した場合、以降に解析するフレームサイズをこれまでのものと同じにするか、今回の違うフレームサイズにするかを選択できます。
  --mean_BG_file, -o, (config : [output], mean_BG_file_path)
    出力するバックグラウンドの平均値のフレーム（バックグラウンド平均）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、バックグラウンドの平均値のフレームのファイルは出力されません。
  --std_BG_file, (config : [output], std_BG_file_path)
    出力するバックグラウンドの標準偏差のフレーム（バックグラウンド標準偏差）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、バックグラウンドの標準偏差のフレームのファイルは出力されません。
  --kurtosis_BG_file, (config : [output], kurtosis_BG_file_path)
    出力するバックグラウンドの尖度のフレーム（バックグラウンド尖度）のファイルのパスを指定できます。拡張子は「.fits」にしてください。「None」を指定、または、何も指定しなければ、バックグラウンドの尖度のフレームのファイルは出力されません。標準偏差が0のピクセルは、尖度の解析結果がnanになります。


3. gen_BG_stats.py
  バックグラウンドの統計情報（平均値、標準偏差など）を求め、INIファイルに出力します。
3.1 条件式に使える値
  X : ピクセルのX座標
  Y : ピクセルのY座標
  mean : ピクセルのバックグラウンド平均
  std : ピクセルのバックグラウンド標準偏差
  kurtosis : ピクセルのバックグラウンド尖度
3.2 引数
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --input_directory, -i, (config : [input], directory_path)
    gen_mean_BG_frame_single.pyのものと同様です。
  --mean_BG, -m, (config : [input], mean_BG_file_path)
    バックグラウンド平均ファイルのパスを指定できます。出力される統計情報はフレームからバックグラウンド平均を差し引いたPHのものです。「None」を指定、または、何も指定しなければ、フレームからバックグラウンド平均を引かずに、統計量を解析します。このとき、--valid_pixelでバックグラウンド平均の条件を加えるとエラーとなります。
  --std_BG_file, -std, (config : [input], std_BG_file_path)
    バックグラウンド標準偏差ファイルのパスを指定できます。--valid_pixelでバックグラウンド標準偏差による条件を加える際、指定してください。「None」を指定、または、何も指定しないで--valid_pixelでバックグラウンド標準偏差の条件を加えるとエラーとなります。
  --kurtosis_BG_file, -kurtosis, (config : [input], kurtosis_BG_file_path)
    バックグラウンド尖度ファイルのパスを指定できます。--valid_pixelでバックグラウンド尖度による条件を加える際、指定してください。「None」を指定、または、何も指定しないで--valid_pixelでバックグラウンド尖度の条件を加えるとエラーとなります。
  --valid_pixel, (config : [input], valid_pixel)
    解析に含むピクセルの条件を指定できます。条件式はPythonの表現方法で指定してください。「かつ」と「または」は「*」と「+」で表現してください。条件式に使う値は3.1 を参照してください。
    例）(mean<4000) * (std<100)
    「None」を指定、または、何も指定しなければ、全てのピクセルを計算に含めます。
  --event_list_file, (config : [input], event_list_file_path)
    イベントリストファイルのパスを指定することで、フレームの中にあるイベントを取り除いて解析できます。取り除く範囲はイベントリストのヘッダーのMAXLEAKに依存します。
    例）MAXLEAK=4 => 取り除く範囲 : 9x9ピクセル
    「None」を指定、または、何も指定しなければ、フレームの中にイベントはないものとみなし、全てのピクセルが解析に使用されます。
  --exclude_rim, (config : [input], exclude_rim)
    イベントが含まれているフレームを解析する際、イベントリストに含まれておらずイベントが残ってしまうフレームの端を除外するかどうかを指定できます。「True」を指定、または何も指定しなければ、フレームの端を除外します。除外される端の幅は--event_list_fileで指定されたイベントリストファイルのMAXLEAK*2-1ピクセルです。「True」以外を指定すれば、端を除去せずに解析します。
  --limit_frame_num, (config : [input], limit_frame_num)
    gen_mean_BG_frame_single.pyのものと同様です。
  --match_file_name, (config : [input], match_file_name)
    gen_mean_BG_frame_single.pyのものと同様です。
  --HDU_index, (config : [input], HDU_index)
    gen_mean_BG_frame_single.pyのものと同様です。
  --valid_frame_shape, (config : [input], valid_frame_shape)
    解析するフレームのサイズ（ピクセル数）を指定できます。--input_directoryで指定したディレクトリの中にあるフレームのサイズが混在している場合、--valid_frame_shapeで指定されたサイズのフレームが解析されます。指定の仕方は「[高さ(Yの大きさ)]x[幅(Xの大きさ)]」としてください。
    例）2040x2048
    その他にも、「\d+ *[x|X|,] *\d+」でマッチする文字列ならば構いません。
    例）2040,2048
    「None」を指定、または、何も指定しなければ、--mean_BGで指定したバックグラウンド平均のピクセル数を指定したとみなします。--mean_BGで何も指定していなければ、--match_file_nameでマッチするファイルのうち、辞書順の一番先頭のファイル名のフレームのサイズを指定したとみなします（その際、一度そのファイルを読み込むことになります）。
  --invalid_shape_process, (config : [input], invalid_shape_process)
    gen_mean_BG_frame_single.pyのものと同様です。
  --BG_stats_file, -o, (config : [output], BG_stats_file_path)
      出力するバックグラウンドの統計情報が入ったファイルのパスを指定できます。拡張子は「.ini」にしてください。「None」を指定、または、何も指定しなければ、バックグラウンドの統計情報が入ったファイルは出力されません。


4. gen_BG_spectrum.py
  バックグラウンドのスペクトル（ヒストグラム）を描いたファイルを出力します。
4.1 ビンの区切りに使える定数
  num_sample : バックグラウンド統計情報を求める
  sum_PH : PHの合計
  sum_square_PH : PH^2の合計
  sum_cubic_PH : PH^3の合計
  sum_biquadratic_PH : PH^4の合計
  mean_PH : PHの平均
  std_PH : PHの標準偏差
  kurtosis_PH : PHの尖度
  max_PH : PHの最大値
  min_PH : PHの最小値
4.2 引数
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --input_directory, -i, (config : [input], directory_path)
    gen_mean_BG_frame_single.pyのものと同様です。
  --mean_BG, -m, (config : [input], mean_BG_file_path)
    バックグラウンド平均ファイルのパスを指定できます。出力されるスペクトルはフレームからバックグラウンド平均を差し引いた値のものです。「None」を指定、または、何も指定しなければ、フレームからバックグラウンド平均を引かずに、解析します。このとき、--valid_pixelでバックグラウンド平均の条件を加えるとエラーとなります。
  --std_BG_file, (config : [input], std_BG_file_path)
    gen_BG_stats.pyのものと同様です。
  --kurtosis_BG_file, (config : [input], kurtosis_BG_file_path)
    gen_BG_stats.pyのものと同様です。
  --event_list_file, (config : [input], event_list_file_path)
    gen_BG_stats.pyのものと同様です。
  --exclude_rim, (config : [input], exclude_rim)
    gen_BG_stats.pyのものと同様です。
  --BG_stats_file, --st, (config : [input], BG_stats_file_path)
    バックグラウンド統計情報ファイルのパスを指定できます。バックグランド統計情報は--binsで使うバックグラウンドの統計情報として使われます。「None」を指定、または、何も指定しなければ、バックグラウンド統計情報を解析してからビンの区切りかたの設定をするので、2回ずつフレームを読み込むことになります。
  --valid_pixel, (config : [input], valid_pixel)
    gen_BG_stats.pyのものと同様です。
  --bins, -b, (config : [input], bins)
    ビンの区切りかたを指定できます。Pythonにおける配列を入力してください（Numpyの関数、配列でも可）。
    例）
      range(0, 4096)
      linspace(0.0, 4096.0, 400)
    また、定数として、バックグラウンド統計情報の値を使うことができます。バックグラウンド統計情報の値は4.1 を参照してください。
    例）
      linspace(ceil(min_PH), floor(max_PH)+1, 400)
    何も指定しなければ、「arange(ceil(min_PH)-1, floor(max_PH) + 2)」（PHの最小値の小数点以下切り捨て（最小値が整数ならば最小値-1）から最大値の小数点以下切り上げ（整数ならば最大値+1）までを1区切りしたビン）を指定したとみなします。
  --y_scale, -ys, (config : [input], y_scale)
    y軸の表示スケール（リニア、対数）を指定できます。リニアは「lin」、対数は「log」と指定してください。何も指定しなければ、「log」を指定したとみなします
  --x_label, (config : [input], x_label)
    スペクトルの横軸ラベル名を指定できます。何も指定しなければ、「PHasum [ch]」を指定したとみなします。
  --y_label, (config : [input], y_label)
    スペクトルの縦軸ラベル名を指定できます。何も指定しなければ、「intensity [counts/bin]」を指定したとみなします。
  --limit_frame_num, (config : [input], limit_frame_num)
    gen_mean_BG_frame_single.pyのものと同様です。
  --match_file_name, (config : [input], match_file_name)
    gen_mean_BG_frame_single.pyのものと同様です。
  --HDU_index, (config : [input], HDU_index)
    gen_mean_BG_frame_single.pyのものと同様です。
  --valid_frame_shape, (config : [input], valid_frame_shape)
    gen_mean_BG_stats.pyのものと同様です。
  --color, (config : [input], color)
    スペクトルの色を指定できます。「red」、「green」、「blue」、「cyan」などの色名か、「(255,0,0)」、「(0,255,0)」、「(0,0,255)」などの「()」と整数（0〜255）と「,」でRGB値で指定してください。何も指定しなければ、「red」を指定したとみなします。
  --invalid_shape_process, (config : [input], invalid_shape_process)
    gen_mean_BG_frame_single.pyのものと同様です。
  --BG_spectrum_file, -o, (config : [output], BG_spectrum_file_path)
    出力するバックグラウンドスペクトルファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、バックグラウンドスペクトルファイルは出力されません。


5. gen_threshold.py
  バックグラウンド統計情報からevent_thとsplit_thを計算し、thresholdファイルを出力します。
5.1 引数
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --BG_stats_file, -i, (config : [input], BG_stats_file_path)
    バックグラウンド統計情報ファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、thresholdファイルを出力せず終了します。
  --threshold_mode, -m, (config : [input], threshold_mode)
    解析の方法を指定できます。「default」を指定、または、何も指定しなければ、バックグラウンドの標準偏差をσとしてevent_th=10σ、split_th=3σとします。「t」または「student_t」を指定すればt分布を仮定した解析をします。
  --threshold_file, -o, (config : [input], thresold_file_path)
    出力するthresholdファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、thresholdファイルは出力されません。


6. gen_event_list.py
  フレーム中のイベントを抽出し、イベントのデータ（フレーム、イベントの中心のピクセル、PHasum、vortex、PH配列）がまとまったイベントリストファイルを出力します。
6.1 引数
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --input_directory, -i, (config : [input], directory_path)
    gen_mean_BG_frame_single.pyのものと同様です。
  --threshold_file, -th, (config : [input], thresold_file_path)
    thresholdファイルのパスを指定することで、event_thとsplit_thを指定できます。ただし、コンフィグファイルやターミナル上でthresholdを指定した場合、そちらが優先されます。「None」を指定、または、何も指定しなければ、コンフィグファイルのevent_th、split_thまたはターミナル上の--event_th、--split_thをthresoldとして解析します。
  --mean_BG_file, -bg, (config : [input], mean_BG_file_path)
    バックグラウンド平均ファイルのパスを指定できます。何も指定しなかった場合、--match_file_nameでマッチするファイルのうち、辞書順の一番先頭と2番目のファイル名のフレームでバックグラウンド平均を計算し、解析に用います。
  --event_th, -eth, (config : [input], event_th)
    event_thを指定できます。「None」を指定、または、何も指定しなければ、--threshold_fileで指定されたパスのファイルを参照し、解析に用います。--threshold_fileも何も指定されていなければ、--match_file_nameでマッチするファイルのうち、辞書順の一番先頭と2番目のファイル名のフレームから標準偏差を計算し、その10倍の値を解析に用います。
  --split_th, -sth, (config : [input], split_th)
    split_thを指定できます。「None」を指定、または、何も指定しなければ、--threshold_fileで指定されたパスのファイルを参照し、解析に用います。--threshold_fileも何も指定されていなければ、--match_file_nameでマッチするファイルのうち、辞書順の一番先頭と2番目のファイル名のフレームから標準偏差を計算し、その3倍の値を解析に用います。
  --max_leak, -ml, (config : [input], max_leak)
    max_leakを指定できます。何も指定しなければ、「1」を指定したとみなします。
  --limit_frame_num, (config : [input], limit_frame_num)
    gen_mean_BG_frame_single.pyのものと同様です。
  --match_file_name, (config : [input], match_file_name)
    gen_mean_BG_frame_single.pyのものと同様です。
  --valid_frame_shape, (config : [input], valid_frame_shape)
    gen_mean_BG_stats.pyのものと同様です。
  --HDU_index, (config : [input], HDU_index)
    gen_mean_BG_frame_single.pyのものと同様です。
  --input_event_list_file, (config : [input], event_list_file_path)
    WARNING!!!
      現在、この引数は解析に未対応なので、何も指定しないでください！
    イベントリストファイルのパスを指定することで、フレーム中のイベントの位置をあらかじめ特定してから解析します。指定したイベントリスト中に存在しないイベントは出力されるイベントリストには含まれません。
  --invalid_shape_process, (config : [input], invalid_shape_process)
    gen_mean_BG_frame_single.pyのものと同様です。
  --event_list_file, -o, (config : [output], event_list_file_path)
    出力するイベントリストファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、イベントリストファイルは出力されません。


7. gen_spectrum.py
  イベントリストからスペクトル（ヒストグラム）を描いたファイル（スペクトルイメージファイル）やスペクトルのビンのデータをFITSにしたファイル（スペクトルバイナリファイル）を出力します。
7.1 スペクトルとして計算できる値
  frame_num : イベントのフレーム番号(0~)
  Y : イベントの中心ピクセルのY
  X : イベントの中心ピクセルのX
  PHausm : PH[0]とPH[i](i=1~)のうち、split_thを超えたものを足し合わせた値
  vortex : イベントの中心の周りの8ピクセルのPHの形状を示す値(0~255、シングルイベントならば0)
  PH[i] : イベントの中心とその周りのPH
  mean_BG[y,x] : イベントの中心とその付近のバックグラウンド平均（mean_BG[Y,X]はイベントの中心のバックグラウンド平均）
  std_BG[y,x] : イベントの中心とその付近のバックグラウンド標準偏差（std_BG[Y,X]はイベントの中心のバックグラウンド標準偏差）
  kurtosis_BG[y,x] : イベントの中心とその付近のバックグラウンド尖度（kurtosis_BG[Y,X]はイベントの中心のバックグラウンド尖度）
  その他、Y+X**2などの数式もスペクトルにすることができます。
  PHはnumpy.ndarrayのメソッドやNumpyの関数を使うこともできます。
  例）PH.max()
7.2 引数
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --event_list_file, -i, (config : [input], event_list_file_path)
    解析するイベントリストファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、解析も出力もせずソフトを終了します。
  --valid_event, -v, (config : [input], valid_event)
    スペクトルに含むイベントの条件を指定できます。条件式はPythonの表現方法で指定してください。「かつ」と「または」は「*」と「+」で表現してください。条件式に使う値はスペクトルとして計算できる値（7.1 参照）を使います。
    例）
      (300<=Y) * (vortex==0) * (std_BG[Y,X]<10.0)
    「None」を指定、または、何も指定しなければ、全てのイベントをスペクトルに含めます。
  --y_scale, -ys, (config : [input], y_scale)
    gen_BG_spectrum.pyのものと同様です。
  --spectrum_value, (config : [input], spectrum_value)
    スペクトルにする値を指定できます（詳細:7.1）。何も指定しなければ、「PHasum」を指定したとみなします。
  --bins, -b, (config : [input], bins)
    ビンの区切りかたを指定できます。Pythonにおける配列を入力してください（Numpyの関数、配列でも可）。
    例）
      range(0, 4096)
      linspace(0.0, 4097.0, 400)
    また、定数として、スペクトルの値の配列を「spectrum_value」、--valid_eventの条件を満たすスペクトルの値の配列を「valid_spectrum_value」としてそれらのメソッドなどを使うことができます。
    例）
      linspace(valid_spectrum_value.min(), valid_spectrum_value.max(), 400)
    何も指定しなければ、「arange(ceil(valid_spectrum_value.min())-1, floor(valid_spectrum_value.max()) + 2)」（valid_spectrum_valueの最小値の小数点以下切り捨て（最小値が整数ならば最小値-1）から最大値の小数点以下切り上げ（整数ならば最大値+1）までを1区切りしたビン）、指定したとみなします。
  --x_label, (config : [input], x_label)
    gen_BG_spectrum.pyのものと同様です。
  --y_label, (config : [input], y_label)
    gen_BG_spectrum.pyのものと同様です。
  --event_th, -eth, (config : [input], event_th)
    event_thを指定できます。PH[0]がevent_thを超えていないイベントはスペクトルに含まれません。「default」を指定、または、何も指定しなければ、--event_list_fileで指定されたイベントリストファイルのヘッダーのEVENT_THの値を指定したとみなします。
  --split_th, -sth, (config : [input], split_th)
    split_thを指定できます。「default」を指定、または、何も指定しなければ、--event_list_fileで指定されたイベントリストファイルのヘッダーのSPLIT_THの値を指定したとみなします。vortexやPHasumはここで指定された値で再度計算されます。Noneを指定した場合、vortexは全て255になります。
  --color, (config : [input], color)
    gen_BG_spectrum.pyのものと同様です。
  --max_leak, -ml, (config : [input], max_leak)
    PHasumを計算するmax_leakを指定できます。「default」を指定、または、何も指定しなければ、--event_list_fileで指定されたイベントリストファイルのヘッダーのMAXLEAKの値を指定したとみなします。「default」の値よりも大きな値を指定した場合、「default」を指定したとみなします。
  --mean_BG, (config : [input], mean_BG_file_path)
    バックグラウンドの平均値のファイルを指定できます。--spectrum_valueや--valid_eventに用いる際に指定してください。
  --std_BG, (config : [input], std_BG_file_path)
    バックグラウンドの平均値のファイルを指定できます。--spectrum_valueや--valid_eventに用いる際に指定してください。
  --kurtosis_BG, (config : [input], kurtosis_BG_file_path)
    バックグラウンドの平均値のファイルを指定できます。--spectrum_valueや--valid_eventに用いる際に指定してください。
  --spectrum_img_file, -o, (config : [output], spectrum_file_path)
    出力するスペクトルイメージファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、スペクトルイメージファイルは出力されません。
  --spectrum_bin_file, -o, (config : [output], spectrum_file_path)
    出力するスペクトルバイナリファイルのパスを指定できます。「None」を指定、または、何も指定しなければ、スペクトルバイナリファイルは出力されません。

8. gen_spectrums.py
  スペクトルを重ねて描いたスペクトルファイルを出力します。
8.1 引数（ターミナル）
  --config_file, -c
    gen_mean_BG_frame_single.pyのものと同様です。
  --spectrum_file, -o, (config : [output], spectrum_file_path)
    gen_spectrum.pyのものと同様です。
8.2 引数（コンフィグファイル）
  [input], config_file_[n]
    gen_spectrum.pyで読み込むコンフィグファイルを指定してください。[n]は1から始まる整数で、連続した数値で項目を追加してください。
    例）
      [input]
      config_file_1 = spectrum_config_20191004.ini
      config_file_2 = spectrum_config_20191005.ini
      config_file_3 = spectrum_config_20191006.ini
    スペクトルは[n]が小さい順に上から描かれます。
  [input], auto_color_set
    スペクトルの色を自動で設定するかを指定できます。「True」を指定すれば、色は自動で設定されます。このときのスペクトルの色は、[input], config_file_[n]に依存します。[n]が1のスペクトルを赤として始め、色相環を[n]の個数で等分したものになります。
    例）
      コンフィグファイル
        [input]
        auto_color_set = True
        config_file_1 = spectrum_config_20191004.ini
        config_file_2 = spectrum_config_20191005.ini
        config_file_3 = spectrum_config_20191006.ini
      のとき、spectrum_config_20191004.iniは赤、spectrum_config_20191005.iniは緑、spectrum_config_20191006.iniは青で描かれます。
    「True」以外を指定すれば、[input], config_file_[n]で読み込まれるコンフィグファイルの[input], colorでスペクトルが描かれます。
8.3 凡例（ラベル名）
  凡例の指定はgen_spectrum.pyで読み込むコンフィグファイルで指定してください。[input], labelで指定できます。
  例）
    [input]
    label = vortex:1
