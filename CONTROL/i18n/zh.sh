# 简体中文 texts of the package scripts (generated)
msg_zh() {
	case "$1" in
	title_install)   echo "安装" ;;
	title_update)    echo "从 %s 更新到 %s" ;;
	title_reinst)    echo "重新安装" ;;
	title_remove)    echo "卸载" ;;
	files_ok)        echo "插件文件已安装" ;;
	files_bad)       echo "插件文件不完整 - 请重新安装" ;;
	langs)           echo "语言：%s" ;;
	kept)            echo "设置和交换文件已保留" ;;
	swap_active)     echo "交换已启用：%s (%s MB)" ;;
	swap_none)       echo "尚无已启用的交换" ;;
	ram)             echo "内存：%s MB" ;;
	zram_yes)        echo "zram（压缩内存）：支持" ;;
	zram_no)         echo "zram（压缩内存）：此内核不支持" ;;
	restart)         echo "请重启界面以加载插件：" ;;
	restart_upd)     echo "请重启界面以加载新版本：" ;;
	restart_rm)      echo "请重启界面以卸载插件：" ;;
	restart_menu)    echo "MENU > 待机 / 重启 > 重启图形界面" ;;
	restart_cmd)     echo "或在终端中：" ;;
	find_it)         echo "之后可以在插件浏览器以及以下位置找到它：" ;;
	find_path)       echo "MENU > 设置 > 系统 > 存储设备 > Simple Swap Manager" ;;
	rm_done)         echo "插件已卸载" ;;
	rm_swap_on)      echo "交换文件将保持启用直到下次重启：%s (%s MB)" ;;
	rm_swap_kept)    echo "交换文件仍保留在存储设备上：%s" ;;
	rm_no_boot)      echo "启动时将不再启用。" ;;
	rm_delete)       echo "删除并释放磁盘空间：" ;;
	rm_zram)         echo "zram 将保持启用直到下次重启" ;;
	experimental)    echo "DreamOS 实验版 - 请反馈问题" ;;
	esac
}
