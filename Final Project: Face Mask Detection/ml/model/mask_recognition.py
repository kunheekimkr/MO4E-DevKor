## Code Referenced from https://pseudo-lab.github.io/Tutorial-Book/chapters/object-detection/Ch5-Faster-R-CNN.html


import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
import torch
import torchvision
from torchvision import transforms, models
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

def get_model_instance_segmentation(num_classes):
  
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model

def make_prediction(model, img, threshold):
    model.eval()
    preds = model(img)
    for id in range(len(preds)) :
        idx_list = []

        for idx, score in enumerate(preds[id]['scores']) :
            if score > threshold : 
                idx_list.append(idx)

        preds[id]['boxes'] = preds[id]['boxes'][idx_list]
        preds[id]['labels'] = preds[id]['labels'][idx_list]
        preds[id]['scores'] = preds[id]['scores'][idx_list]

    return preds

def plot_image_from_output(img, pred):
    
    img = img.cpu().permute(1,2,0)
    
    fig,ax = plt.subplots(1)
    ax.imshow(img)
    
    for idx in range(len(pred["boxes"])):
        xmin, ymin, xmax, ymax = pred["boxes"][idx]

        if pred['labels'][idx] == 1 :
            rect = patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),linewidth=1,edgecolor='r',facecolor='none')
        
        elif pred['labels'][idx] == 2 :
            
            rect = patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),linewidth=1,edgecolor='g',facecolor='none')
            
        else :
        
            rect = patches.Rectangle((xmin,ymin),(xmax-xmin),(ymax-ymin),linewidth=1,edgecolor='orange',facecolor='none')

        ax.add_patch(rect)

    plt.axis('off')

    plt.savefig('output.png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()


def mask_recognition(original_img):
    data_transform = transforms.Compose([  # transforms.Compose : list 내의 작업을 연달아 할 수 있게 호출하는 클래스
        transforms.ToTensor() # ToTensor : numpy 이미지에서 torch 이미지로 변경
    ])
    model = get_model_instance_segmentation(4)
    device = torch.device('cpu')
    model.to(device)
    model.load_state_dict(torch.load(f'model/model_10.pt', map_location=device))

    # Create Prediction on sample.png   
    with torch.no_grad():
    
        img = data_transform(original_img).to(device)
        img = img.unsqueeze(0)

        pred = make_prediction(model, img, 0.5)
        img = img.squeeze(0)
        plot_image_from_output(img, pred[0])