from angle_emb import AnglE
from scipy import spatial


def test():
    angle = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()
    doc_vecs = angle.encode([
        'The weather is great!',
        'The weather is very good!',
        'i am going to bed'
    ])

    for i, dv1 in enumerate(doc_vecs):
        for dv2 in doc_vecs[i + 1:]:
            print(1 - spatial.distance.cosine(dv1, dv2))


if __name__ == '__main__':
    test()
