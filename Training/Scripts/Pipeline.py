import operator

from dataloader import Data
from DetectionModels import *
from SubModels import *
from Training import *

def main():
    # Alexnet3
    # Threshold
    # All SubModels
    # Max is label
    # Compare with test label, can be 0
    # Load our test data
    
    """ FINAL MODEL PATHS HERE """
    # Detector
    detect_path = r"../Models/detect_alex3, imgs=27k, bs=128, epoch=20, lr=0.0001/19_epoch.pt" 
    model_detect = torch.load(detect_path).cuda()
    # Following are hem type models
    # TODO CONFIRM PATH
    # TODO THIS MODEL NAME IS WEIRD
    subdural_path = r"../Models/AlexNetEpidural, imgs=27k, bs=256, epoch=30, lr=0.0001/29_epoch.pt" 
    model_subdural = torch.load(subdural_path).cuda()

    intrav_path = r"../Models/AlexNetIntrav, imgs=27k, bs=256, epoch=30, lr=0.0001/29_epoch.pt" 
    model_intrav = torch.load(intrav_path).cuda()

    subara_path = r"../Models/AlexNetSubara, imgs=27k, bs=256, epoch=30, lr=0.0001/29_epoch.pt" 
    model_subara = torch.load(subara_path).cuda()

    intrap_path = r"../Models/AlexNetIntrap, imgs=27k, bs=256, epoch=30, lr=0.0001/29_epoch.pt" 
    model_intrap = torch.load(intrap_path).cuda()
    hem_types = { model_subdural : "subdural", model_intrav : "intraventricular", model_subara : "subarachnoid", model_intrap : "intraparenchymal"]
    """ FINAL MODEL PATHS """

    test = [
        "../../Data/Processed/test/epidural",
        "../../Data/Processed/test/intraparenchymal",
        "../../Data/Processed/test/subarachnoid",
        "../../Data/Processed/test/intraventricular",
        "../../Data/Processed/test/subdural",
        "../../Data/Processed/test/nohem",    
    ]
    # Do not replace any label
    test_data = Data(test, maximum_per_folder = 1500,  tl_model = "alexnet", in_channels=3)
    # Batch size of 1 to simplify
    test_loader = torch.utils.data.DataLoader(test_data, batch_size= 1)
    threshold = 0.2
    # Iterate through test_data
    correct = 0
    total = 0
    for img, label in test_data_loader:
        #To Enable GPU Usage
        img = img.cuda()
        label = label.cuda()
        #############################################
        hem_detected = model_detect(img)
        if hem_detected > threshold:
            predictions = {}
            for model, pred_label in hem_types.items():
                predictions[pred_label] = model(img)
            # Get probability of Epidural
            epidural_prob = 0.0
            for _, prob in predictions.items():
                epidural_prob += prob
            predictions["epidural"] = 1 - epidural_prob
            # Get maxiumum probability
            predicted_label = max(predictions, key=predictions.get)
        else:
            # TODO 
            predicted_label = "no_hem"

        if predicted_label == label:
            correct += 1
        total += 1
    
    print("Test Accuracy is : " + str(correct/total))

if __name__ == "__main__":
    main()