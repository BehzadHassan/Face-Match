import torch
import cv2
from facenet_pytorch import InceptionResnetV1, MTCNN
from sklearn.metrics.pairwise import cosine_similarity

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the MTCNN face detector
mtcnn = MTCNN(keep_all=True, device=device)

# Load the FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)


def preprocess_image(image_path):
    """Load and preprocess the image for face detection and embedding."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    return img


def get_face_embedding(image_path):
    """Get face embeddings from the input image."""
    img = preprocess_image(image_path)

    # Detect faces
    boxes, _ = mtcnn.detect(img)

    if boxes is not None:
        # Get the face embeddings for each detected face
        faces = mtcnn(img)
        embeddings = model(faces).detach().cpu().numpy()
        return embeddings
    else:
        return None  # No faces found


def compare_faces(embedding1, embedding2):
    """Compare two face embeddings using cosine similarity."""
    # Calculate the cosine similarity
    similarity = cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))
    return similarity[0][0]  # Return the similarity score


def MatchFaces(image_path1, image_path2):
    # Example usage: compare two images

    embedding1 = get_face_embedding(image_path1)
    embedding2 = get_face_embedding(image_path2)

    if embedding1 is not None and embedding2 is not None:
        # Compare the embeddings
        similarity_score = compare_faces(embedding1[0], embedding2[0])
        # print(f'Similarity score between the two images: {similarity_score}')
        # Set a threshold for recognizing if the faces match
        threshold = 0.6  # You can adjust this value based on your needs
        if similarity_score > threshold:
            return True
        else:
            return False
    else:
        return False
