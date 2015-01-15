QUE_PRESERVE = ['atque', 'quoque', 'neque', 'itaque', 'absque',
                'apsque', 'abusque', 'adaeque', 'adusque', 'denique', 'deque',
                'susque', 'oblique', 'peraeque', 'plenisque', 'quandoque',
                'quisque', 'quaeque', 'cuiusque', 'cuique', 'quemque', 'quamque',
                'quaque', 'quique', 'quorumque', 'quarumque', 'quibusque', 'quosque',
                'quasque', 'quotusquisque', 'quousque', 'ubique', 'undique',
                'usque', 'uterque', 'utique', 'utroque', 'utribique', 'torque',
                'coque', 'concoque', 'contorque', 'detorque', 'decoque', 'excoque',
                'extorque', 'obtorque', 'optorque', 'retorque', 'recoque',
                'attorque', 'incoque', 'intorque', 'praetorque'
                ]


def strip_enclitic_que(tokens, strip=True):
    if strip:
        result_tokens = []
        for t in tokens:
            if t.endswith('que') and t not in QUE_PRESERVE:
                result_tokens.append(t.replace('que',''))
                result_tokens.append('-que')
            else:
                result_tokens.append(t)
        return result_tokens
    else:
        return tokens
