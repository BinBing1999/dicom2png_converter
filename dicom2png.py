from pydicom import dcmread
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from tkinter import filedialog
import tkinter


#用户界面参量：维度号码，通道类型、输入路径、输出路径
#word内提醒医生必须选中dicom文件，其他格式不行#必须确认导入导出文件夹标准化（输入只有dicom，输出只有空文件夹），重新生成的话必须手动删除文件夹内容或者新建文件夹（不搞一键删除）


#可持续优化：图像通道不是RGB而是BGR/GBR的问题#注意uniT8的精度#内存目前最大占用1g

#parameters that need to be set at beginning

#set by programmer-----------------------------!
MAX_STANDARD=255
MIN_STANDARD=0

Channel_Mode=1#1 or 3 symbolizes one channel or RGB channel
Main_Dimens=0#0/1/2 means which 2-dimens is front
address=''              #change path    always remember add a 
save_address=''             #change path
print("Welcome to Dicom-Transformer.")
#def is_dicom_file(filename):
#    '''
#       判断某文件是否是dicom格式的文件
#    :param filename: dicom文件的路径
#    :return:
#    '''
#    file_stream = open(filename, 'rb')
#    file_stream.seek(128)
#    data = file_stream.read(4)
#    file_stream.close()
#    if data == b'DICM':
#        return True
#    return False


def DICOM_to_PNG(address,save_address):
    print('All Dicom file names: ',os.listdir(address))
    all_data_name=os.listdir(address)
    print('Total DICOM Files:',len(all_data_name))

    for i in range(len(all_data_name)):
        path=address+all_data_name[i]
        ds=dcmread(path)
        print(f'Dealing with file {all_data_name[i]}.')
        print(ds.PatientName)
        print(ds.Manufacturer)
        print(ds.InstitutionName)
        print(f'{all_data_name[i]} got shape {ds.pixel_array.shape}, its dimensions is {ds.pixel_array.ndim}, the type of matrix is {type(ds.pixel_array)}.')#numpy.ndarray type
        ds.pixel_array_uint8=(ds.pixel_array).astype(np.uint8)#faster  uinT8  precision problem
        print('MAX PIXEL VALUE:',np.max(ds.pixel_array_uint8), '  MIN PIXEL VALUE:',np.min(ds.pixel_array_uint8))
        
        print('Image processing...')
        if np.max(ds.pixel_array_uint8)>MAX_STANDARD or np.min(ds.pixel_array_uint8)<MIN_STANDARD:
            ds_nor=((ds.pixel_array_uint8/np.max(ds.pixel_array_uint8))*MAX_STANDARD).astype('uint8')
        else:
            ds_nor=ds.pixel_array_uint8


        if Channel_Mode == 1:#grey
            ds_nor_3dimens=ds_nor[:,:,:,0]
            for j in range(ds_nor_3dimens.shape[Main_Dimens]):#循环对每一层转换，名字加个层数号
                if Main_Dimens==0:
                    ds_nor_layer=ds_nor_3dimens[j,:,:]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer)
                    im.save(save_name)
                if Main_Dimens==1:
                    ds_nor_layer=ds_nor_3dimens[:,j,:]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer)
                    im.save(save_name)
                if Main_Dimens==2:
                    ds_nor_layer=ds_nor_3dimens[:,:,j]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer)
                    im.save(save_name)
        else:#RGB
            #ds_nor
            for j in range(ds_nor.shape[Main_Dimens]):#循环对每一层转换，名字加个层数号
                if Main_Dimens==0:
                    ds_nor_layer=ds_nor[j,:,:,:]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer,mode='RGB')#mode='RGB'
                    im.save(save_name)
                if Main_Dimens==1:
                    ds_nor_layer=ds_nor[:,j,:,:]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer,mode='RGB')#mode='RGB'
                    im.save(save_name)
                if Main_Dimens==2:
                    ds_nor_layer=ds_nor[:,:,j,:]
            
                    save_name=save_address+all_data_name[i]+'_'+str(j)+'.png'
       
                    im=Image.fromarray(ds_nor_layer,mode='RGB')#mode='RGB'
                    im.save(save_name)
        print(f'{all_data_name[i]} done.\n\n')


def get_input_info():
    global Channel_Mode,Main_Dimens
    #Channel_Mode=channel_list.get(ANCHOR)
    if Channel_variable.get()==1:
        Channel_Mode=int(1)
    if Channel_variable.get()==3:
        Channel_Mode=int(3)

    if Dimens_variable.get()==0:
        Main_Dimens=int(0)
    if Dimens_variable.get()==1:
        Main_Dimens=int(1)
    if Dimens_variable.get()==2:
        Main_Dimens=int(2)
    #Main_Dimens=dimens_list.get(ANCHOR)
    print(Channel_Mode," mode, ",Main_Dimens," is dimension feature.")
    win.destroy()


def directory_in():
    # get a directory path by user
    global address
    address=filedialog.askdirectory(initialdir=r"C:",
                                    title="Select Dicom Input Folder Directory:")
    print("Your input folder path is: ",address)
    input_path=tkinter.Label(win,text=address,font=('italic 14'))
    input_path.grid(row=0,column=2)

def directory_out():
    # get a directory path by user
    global save_address
    save_address=filedialog.askdirectory(initialdir=r"C:",
                                    title="Select Dicom Output Folder Directory:")
    print("Your output folder path is: ",save_address)
    output_path=tkinter.Label(win,text=save_address,font=('italic 14'))
    output_path.grid(row=1,column=2)
    

    


#if __name__ == '__main__':
win = tkinter.Tk()
win.title("Dicom to PNG converter (written by bb)")
win.geometry("600x200+200+50")#change size----------------------------------!

Channel_variable=tkinter.IntVar()
Channel_variable.set(2)
Dimens_variable=tkinter.IntVar()
Dimens_variable.set(4)

input_path_label = tkinter.Label(win,
                      text="Input Dicom Files path:     ",
                      font=("italic 14", 10),
                      justify="left",
                      anchor="center")
input_path_label.grid(row=0,column=0)
dialog_btn1 = tkinter.Button(win, text='Select Folder', command = directory_in)
dialog_btn1.grid(row=0,column=1)


output_path_label = tkinter.Label(win,
                      text="Output Dicom Files path:     ",
                      font=("italic 14", 10),
                      justify="left",
                      anchor="center")
output_path_label.grid(row=1,column=0)
dialog_btn2 = tkinter.Button(win, text='Select Folder', command = directory_out)
dialog_btn2.grid(row=1,column=1)

#channel_list = tkinter.Listbox(win)
#channel_list.grid(row=2,column=1)
#channel_list.insert(1, 'Grey')
#channel_list.insert(3, 'RGB')
#dimens_list = tkinter.Listbox(win)
#dimens_list.grid(row=2,column=2)
#dimens_list.insert(0, '1')
#dimens_list.insert(1, '2')
#dimens_list.insert(2, '3')
channel_label = tkinter.Label(win,
                      text="Channel Type:",
                      font=("italic 14", 10),
                      justify="left",
                      anchor="center")
channel_label.grid(row=2,column=0)
channel_entry1=tkinter.Radiobutton(win, text="Grey", variable=Channel_variable, value=1)
channel_entry2=tkinter.Radiobutton(win, text="RGB", variable=Channel_variable, value=3)
channel_entry1.grid(row=2,column=1)
channel_entry2.grid(row=2,column=2)

dimens_label = tkinter.Label(win,
                      text="Dimension Type:",
                      font=("italic 14", 10),
                      justify="left",
                      anchor="center")
dimens_label.grid(row=3,column=0)
dimens_entry1=tkinter.Radiobutton(win, text="1", variable=Dimens_variable, value=0)
dimens_entry2=tkinter.Radiobutton(win, text="2", variable=Dimens_variable, value=1)
dimens_entry3=tkinter.Radiobutton(win, text="3", variable=Dimens_variable, value=2)
dimens_entry1.grid(row=3,column=1)
dimens_entry2.grid(row=3,column=2)
dimens_entry3.grid(row=3,column=3)


button = tkinter.Button(win, text="Confirm", command=get_input_info)
button.grid(row=5,column=1)
win.mainloop()
if address != "" and save_address != "":
    print("Path directing...")
    DICOM_to_PNG(address+'/',save_address+'/')
    print("All Converted.")
    os.system ("pause")
else:
    print("Incorrect folder path, program ends. Please restart the program and select the legal path.")
    os.system ("pause")

